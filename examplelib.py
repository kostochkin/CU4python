import socket
import sys


class StdioLogger:
    def debug(self, *args):
        print("[DEBUG]", *args, sep=" ", file=sys.stdout)
    
    def warn(self, *args):
        print("[WARN]", *args, sep=" ", file=sys.stderr)
    
    def error(self, *args):
        print("[ERROR]", *args, sep=" ", file=sys.stderr)

    def info(self, *args):
        print("[info]", *args, sep=" ", file=sys.stderr)


class HostIp:
    def __init__(self, addr=None, logger=StdioLogger()):
        self._ip = addr
        self._logger = logger

    def value(self):
        if self._ip is None:
            self._ip = self._detect_ip()
        return self._ip
    
    def _detect_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self._logger.debug("Trying to detect my IP address")
            # Any non-localhost address even non-exsiting
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            self._logger.warn("Failed. Using localhost.")
            IP = '127.0.0.1'
        finally:
            self._logger.debug("Got IP", IP)
            s.close()
        return IP


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
        udpsocket.sendto(self._ip.value().encode(), ('<broadcast>', self._base_port + 1))

    def _bind_and_listen(self, serversocket):
        port = self._base_port + 2
        ip = self._ip.value()
        self._logger.debug("Run listener on", ip, ":", port)
        serversocket.bind((ip, port))
        serversocket.listen(5)
        serversocket.settimeout(self._timeout)

    def __iter__(self):
        return map(lambda x: x[1], self.value())


class CU4Server:
    def __init__(self, ip, port=9876, logger=StdioLogger()):
        self._ip = ip
        self._port = port
        self._logger = logger

    def send_scpi(self, command):
        self._logger.debug("Sending", command)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (self._ip.value(), self._port)
        try:
            sock.connect(addr)
            sock.sendto(command.encode(), addr)
            return sock.recv(1024).decode()
        finally:
            sock.close()

    def devices(self):
        devsb = self.send_scpi("SYST:DEVL?").strip().split("\r\n;<br>")
        return map(self._dev_from_string, devsb[1:])

    def _dev_from_string(self, s):
        params = s.split(": ")
        address = params[1][8:]
        dev_type = params[2][5:]
        return get_dev_class(dev_type)(self, address)

    def ip(self):
        return self._ip


class CU4Device:
    def __init__(self, cu4server, address, logger=StdioLogger()):
        self._cu4server = cu4server
        self._address = address
        self._logger = logger

    def init(self):
        self._logger.debug("Init", self)
        res = self._cu4server.send_scpi("GEN:DEV{}:INIT".format(self._address)).strip()
        self._logger.debug(res)
        return res == "OK"

    def data(self):
        self._logger.debug("Getting data for", self)
        return self._send_command("DATA?")

    def __str__(self):
        return "{}:{}:{}".format(self.__class__.__name__, self._cu4server.ip().value(), self._address)
    
    def __repr__(self):
        return self.__str__()

    def _dev_prefix(self):
        p = self.dev_type()
        a = self._address
        return "{}:DEV{}".format(p, a)

    def _send_command(self, cmd):
        return self._cu4server.send_scpi("{}:{}".format(self._dev_prefix(), cmd)).strip()
    
   
class CU4DeviceSDM(CU4Device):
    def dev_type(self):
        return "SSPD"

class CU4DeviceTDM(CU4Device):
    def dev_type(self):
        return "TEMD"

    def set_thermometer_on(self):
        return self._send_command("THON 1")

    def set_thermometer_off(self):
        return self._send_command("THON 0")

    def is_thermometer_on(self):
        return self._send_command("THON?") == "1"


def get_dev_class(dev_type):
    part = dev_type[:6]
    dev = CU4Device
    if part == "CU4SDM":
        dev = CU4DeviceSDM
    elif part == "CU4TDM":
        dev = CU4DeviceTDM
    return dev
