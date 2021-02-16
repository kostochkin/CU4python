import socket
from cu4lib.simplelog import StdioLogger
from cu4lib.devices.cu4device import CU4Device, CU4DeviceSDM
from cu4lib.devices.temperature_drivers import CU4DeviceTDM0

class HostIp:
    def __init__(self, addr=None, logger=StdioLogger()):
        self._ip = addr
        self._auto = False
        self._logger = logger

    @property
    def value(self):
        if self._ip is None:
            self._ip = self._detect_ip()
        return self._ip
    
    def _detect_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self._logger.debug("Trying to detect my IP address")
            # Any non-localhost address even non-exsiting
            s.connect(('8.8.8.8', 1))
            IP = s.getsockname()[0]
        except Exception:
            self._logger.warn("Failed. Using localhost.")
            IP = '127.0.0.1'
        finally:
            self._logger.debug("Got IP", IP)
            s.close()
        self._auto = True
        return IP

    def __repr__(self):
        v = self.value
        if self._auto:
            a = "Auto"
        else:
            a = "Manual"
        return "<{}IP={}>".format(a, v)


class Cu4ServersList:
    def __init__(self, host_ip=HostIp(), base_port=9876, timeout=3, logger=StdioLogger()):
        self._ip = host_ip
        self._timeout = timeout
        self._base_port = base_port
        self._list = []
        self._logger = logger

    def value(self):
        if not self._list:
            self._enumerate_servers()
        return self._list

    def _enumerate_servers(self):
        new_list = []
        self._logger.debug("Searching for servers...")
        tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            self._bind_and_listen(tcpsocket)
            self._send_broadcast(udpsocket)
            self._logger.debug("Enumerating...")
            while 1:
                try:
                    new_list += self._incoming_to_servers_list(tcpsocket)
                except socket.timeout:
                    if not new_list:
                        self._logger.warn("Servers not found")
                    break
        finally:
            self._logger.debug("Cleanup")
            tcpsocket.close()
            udpsocket.close()
        self._list = new_list
        return self._list
    
    def _incoming_to_servers_list(self, tcpsocket):
        conn, adp = tcpsocket.accept()
        data = conn.recv(1024).decode()
        self._logger.debug("Got datagram", data)
        addr, _ = adp
        if addr in data.split(";"):
            self._logger.info("Found server", addr)
            cu4Server = CU4Server(ip=HostIp(addr), port=self._base_port, logger=self._logger)
            return [(addr, cu4Server)]
        return []

    def _send_broadcast(self, udpsocket):
        udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udpsocket.settimeout(self._timeout)
        udpsocket.bind(("", self._base_port))
        udpsocket.sendto(self._ip.value.encode(), ('<broadcast>', self._base_port + 1))

    def _bind_and_listen(self, serversocket):
        port = self._base_port + 2
        ip = self._ip.value
        self._logger.debug("Run listener on", ip, ":", port)
        serversocket.bind((ip, port))
        serversocket.listen(5)
        serversocket.settimeout(self._timeout)

    def __iter__(self):
        return map(lambda x: x[1], self.value())

    def __repr__(self):
        a = map(repr, self)
        return "<Cu4ServersList [{}]>".format(", ".join(a))


class CU4Server:
    def __init__(self, ip, port=9876, logger=StdioLogger(), timeout=3):
        self._ip = ip
        self._port = port
        self._logger = logger
        self._timeout = timeout

    def send_scpi(self, command):
        self._logger.debug("Sending", command)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self._timeout)
        addr = (self._ip.value, self._port)
        s = b''
        try:
            sock.connect(addr)
            sock.sendto(command.encode(), addr)
            while (s[-2:] != b'\r\n'): 
                s += sock.recv(4196)
            self._logger.debug("Received ({})".format(len(s)), s)
            return s.decode()
        except socket.timeout:
            self._logger.error("Socket timeout")
            return "Server timeout"
        finally:
            sock.close()

    @property
    def modules(self):
        return CU4ModulesList(self)

    def ip(self):
        return self._ip

    def __repr__(self):
        return "<CU4Server ip={}>".format(self._ip)


class CU4ModulesList:
    def __init__(self, cu4server):
        self._cu4server = cu4server

    def __iter__(self):
        devsb = self._cu4server.send_scpi("SYST:DEVL?").strip().split("\r\n;<br>")
        return iter(map(self._dev_from_string, devsb[1:]))

    def _dev_from_string(self, s):
        params = s.split(": ")
        address = params[1][8:]
        dev_type = params[2][5:]
        return CU4Module(dev_type, self._cu4server, address)

    def __str__(self):
        return "<CU4ModulesList [{}]>".format(", ".join(map(str, self)))


class CU4Module:
    def __new__(self, dev_type, cu4server, address):
        print(dev_type)
        part = dev_type[:7]
        dev = CU4Device
        if part == "CU4SDM0":
            dev = CU4DeviceSDM
        elif part == "CU4TDM0":
            dev = CU4DeviceTDM0
        # Not implemented in testing invironment
        # elif part == "CU4TDM1":
        #    dev = CU4DeviceTDM1
        return dev(cu4server, address)

