import socket
from CU4lib.simplelog import EmptyLogger
from CU4lib.devices.td.m0 import CU4TDM0
from CU4lib.devices.sd.m0 import CU4SDM0
from CU4lib.devices.components.descriptors import CU4Module
from CU4lib.servers.cu4module_server import SCPI, CU4ModuleServer

class HostIp:
    """ 
        It encapsulates or autodetect ip address of the host.
        
        .. code-block:: python
            
            from CU4lib import *

            # Autodetection
            h = HostIp() 
            print(h)
            # Encapsualting
            h = HostIp("123.456.789.101")
            print(h)
    """
    def __init__(self, addr=None, logger=None):
        self._ip = addr
        self._auto = False
        self._logger = logger or EmptyLogger()

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


class CU4ServersList:
    """ 
        This class searches servers over an Ethernet.
        It implements the iterator interface, so it can be used in the following way:
        
        .. code-block:: python
            
            from CU4lib import *

            l = Cu4ServersList()
            for server in l:
                print(server)
                # Each server represents an CU4 modular system:
                for module in server.modules:
                    print(module)

            # Cu4ServersList also support indexing:
            l = Cu4ServersList()
            cu_ip = "127.0.0.1"
            # get all modules:
            print(l[cu_ip].modules)
            # get module at address 0:
            print(l[cu_ip][0])
    """
    def __init__(self, host_ip=None, base_port=9876, timeout=3, logger=None):
        self._ip = host_ip or HostIp(logger=logger)
        self._timeout = timeout
        self._base_port = base_port
        self._dict = {}
        self._logger = logger or EmptyLogger()

    def value(self):
        if not self._dict:
            self._enumerate_servers()
        return self._dict

    def __getitem__(self, ip_addr):
        return self.value()[ip_addr]

    def _enumerate_servers(self):
        new_dict = {}
        self._logger.debug("Searching for servers...")
        tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            self._bind_and_listen(tcpsocket)
            self._send_broadcast(udpsocket)
            self._logger.debug("Enumerating...")
            while 1:
                try:
                    new_dict.update(self._incoming_to_servers_dict(tcpsocket))
                except socket.timeout:
                    if not new_dict:
                        # For testing
                        # addr = "127.0.0.1"
                        # new_dict[addr] = CU4Server(ip=HostIp(addr), port=self._base_port, logger=self._logger)
                        self._logger.warn("Servers not found")
                    break
        finally:
            self._logger.debug("Cleanup")
            tcpsocket.close()
            udpsocket.close()
        self._dict = new_dict
        return self._dict
    
    def _incoming_to_servers_dict(self, tcpsocket):
        conn, adp = tcpsocket.accept()
        data = conn.recv(1024).decode()
        self._logger.debug("Got datagram", data)
        addr, _ = adp
        if addr in data.split(";"):
            self._logger.info("Found server", addr)
            cu4Server = CU4Server(ip=HostIp(addr), port=self._base_port, logger=self._logger)
            return {addr: cu4Server}
        return {}

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
        return iter(self.value().values())

    def __repr__(self):
        a = ", ".join(map(repr, self))
        return "[{}]".format(a)


class CU4Server:
    def __init__(self, ip, port=9876, logger=None, timeout=3):
        self._ip = ip
        self._port = port
        self._logger = logger or EmptyLogger()
        self._timeout = timeout
        self._modules = None

    def send_scpi(self, command):
        encoded = command.encode()
        self._logger.debug("Sending", encoded)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self._timeout)
        addr = (self._ip.value, self._port)
        s = b''
        try:
            sock.connect(addr)
            sock.sendto(encoded, addr)
            while (s[-2:] != b'\r\n'): 
                s += sock.recv(4196)
            self._logger.debug("Received ({})".format(len(s)), s)
            return s.decode()
        except socket.timeout:
            self._logger.error("Socket timeout")
            return "Server timeout"
        finally:
            sock.close()

    def __getitem__(self, address):
        return self.modules[address]

    @property
    def modules(self):
        self._modules = self._modules or CU4ModulesList(self)
        return self._modules

    def ip(self):
        return self._ip

    def __repr__(self):
        return "<CU4Server ip={}>".format(self._ip)


class CU4ModulesList(object):
    def __init__(self, cu4server):
        self._cu4server = cu4server
        self._modules = {}

    def __getitem__(self, address):
        return self._enumerate_modules()[address]

    def __iter__(self):
        return iter(self._enumerate_modules().values())

    def _enumerate_modules(self):
        if not self._modules:
            devsb = self._cu4server.send_scpi("SYST:DEVL?").strip().split("\r\n;<br>")
            for a, m in map(self._dev_from_string, devsb[1:]):
                self._modules[a] = m
        return self._modules

    def _dev_from_string(self, s):
        params = s.split(": ")
        address = int(params[1][8:])
        dev_type = params[2][5:]
        return address, cu4Module(dev_type, self._cu4server, address)

    def __str__(self):
        return "[{}]".format(", ".join(map(str, self._enumerate_modules().values())))


def cu4Module(dev_type, cu4server, address):
    scpi = SCPI(cu4server)
    part = dev_type[:7]
    if part == "CU4SDM0":
        dev = CU4SDM0
    elif part == "CU4TDM0":
        dev = CU4TDM0
    elif part == "CU4TDM1":
        dev = CU4TDM1
    else:
        dev = CU4Module
    return dev(CU4ModuleServer(scpi, address, dev_type))

