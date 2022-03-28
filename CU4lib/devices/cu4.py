from .td import CU4TDM0, CU4TDM0Data, CU4TDM1
from .sd import CU4SDM0, CU4SDM1
from ..servers.cu4module_server import CU4Messenger, SYST, GEN, DEVT, DEV, CU4CommandMessenger
from ..servers.scpi import COM


class ModuleNotInstalled(Exception):
    pass


class CU4(object):
    def __init__(self, scpi_server, attempts=1):
        self._scpi = scpi_server
        self._messenger = CU4Messenger(self._scpi, attempts=attempts)
        self._syst = CU4CommandMessenger(SYST(), self._messenger)
        self._modules = {}

    def add_module(self, address):
        self.add_modules([address])

    def add_modules(self, adresses):
        for n in adresses:
            self._syst.set(COM("DEVL") & COM("ADD"), str(n))
        self._syst.set(COM("DEVL") & COM("SAVE"))

    @property
    def address(self):
        return self._scpi.address

    @property
    def modules(self):
        return self._enumerate_modules().values()

    @property
    def action_failed(self):
        return self._syst.action_failed

    def __getitem__(self, address):
        return self._cached_module(address)

    def __contains__(self, address):
        try:
            self[address]
            return True
        except ModuleNotInstalled:
            return False

    def __iter__(self):
        return iter(self._cached_modules().values())

    def _cached_modules(self):
        if not self._modules:
            return self._enumerate_modules()
        return self._modules
    
    def _cached_module(self, address):
        if address not in self._modules and not in self._enumerate_modules():
            raise ModuleNotInstalled("Address={}".format(address))
        return self._modules[address]

    def _enumerate_modules(self):
        self._modules = {}
        devsb = self._syst.get(COM("DEVL"))
        for m in map(self._dev_from_string, devsb[1:]):
            self._modules.update(m)
        return self._modules

    def _dev_from_string(self, s):
        params = s.split(": ")
        address = int(params[1][8:])
        dev_type = params[2][5:]
        return {address: _cu4Module(dev_type, self._messenger, address)}

    def __repr__(self):
        return "<CU4 {} [{}]>".format(self.address, ", ".join(map(str, self)))


def _cu4Module(dev_type, messenger, address):
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
    devaddr = DEV(address)
    genserver = CU4CommandMessenger(GEN() & devaddr, messenger)
    devserver = CU4CommandMessenger(DEVT(dev_type) & devaddr, messenger)
    return dev(genserver, devserver, address)
