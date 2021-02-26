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
        self._addr_sock = None

    def _init_socket(self):
        if self._addr_sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self._timeout)
            addr = (self._ip.value, self._port)
            sock.connect(addr)
            self._addr_sock = addr, sock
        return self._addr_sock

    def _close_socket(self):
        _, sock = self._addr_sock
        sock.close()
        self._addr_sock = None

    def send_r(self, command):
        self.send(command)
        return self.receive()

    def send(self, command):
        encoded = command.encode()
        self._logger.debug("Sending", encoded)
        s = b''
        addr, sock = self._init_socket()
        try:
            n = sock.sendto(encoded, addr)
            self._logger.debug("Sent", n)
            return n
        except socket.timeout:
            self._logger.error("Socket timeout")
            self._close_socket()
            return "Server timeout"
    
    def receive(self, n=4196):
        addr, sock = self._init_socket()
        try:
            s = sock.recv(n)
            self._logger.debug("Received ({})".format(len(s)), s)
            return s.decode()
        except socket.timeout:
            self._logger.error("Socket timeout")
            self._close_socket()
            return "Server timeout"

    @property
    def modules(self):
        self._modules = self._modules or CU4ModulesList(self)
        return self._modules

    def ip(self):
        return self._ip
    
    def __getitem__(self, address):
        return self.modules[address]


class CU4ModulesList(object):
    def __init__(self, cu4server):
        self._scpi = SCPI(cu4server)
        self._modules = {}

    def add_address(self, n):
        self._add(n)
        self.save()

    def add_addresses(self, ns):
        for n in ns:
            self._add(n)
        self.save()

    def _add(self, n):
        self._scpi.set(["SYST", "DEVL", "ADD"], [str(n)])

    def save(self):
        self._scpi.set(["SYST", "DEVL", "SAVE"], [])

    def __getitem__(self, address):
        return self._enumerate_modules()[address]

    def __iter__(self):
        return iter(self._enumerate_modules().values())

    def _enumerate_modules(self):
        if not self._modules:
            devsb = self._scpi.get(["SYST", "DEVL"])
            for a, m in map(self._dev_from_string, devsb[1:]):
                self._modules[a] = m
        return self._modules

    def _dev_from_string(self, s):
        params = s.split(": ")
        address = int(params[1][8:])
        dev_type = params[2][5:]
        return address, cu4Module(dev_type, self._scpi, address)

    def __str__(self):
        return "[{}]".format(", ".join(map(str, self._enumerate_modules().values())))


def cu4Module(dev_type, scpi, address):
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

