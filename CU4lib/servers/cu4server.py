import socket
from ..simplelog import EmptyLogger
from .cu4module_server import SCPI, CU4ModuleServer
from ..devices.td import CU4TDM0, CU4TDM1
from ..devices.sd import CU4SDM0, CU4SDM1


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
    elif part == "CU4SDM1":
        dev = CU4SDM1
    elif part == "CU4TDM0":
        dev = CU4TDM0
    elif part == "CU4TDM1":
        dev = CU4TDM1
    else:
        dev = CU4Module
    return dev(CU4ModuleServer(scpi, address, dev_type))

