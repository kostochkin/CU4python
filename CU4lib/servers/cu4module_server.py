from .scpi import COM

class UnsupportedModuleType(Exception):
    pass


class UnknownCommandException(Exception):
    pass


class CU4CommandMessenger(object):
    def __init__(self, prefix, messenger=None):
        self._m = messenger
        self._p = prefix

    @property
    def action_failed(self):
        return self._m.req_failed

    def get(self, cmd_l):
        return self._m.get(self._p & cmd_l)

    def set(self, cmd_l, *param_l):
        return self._m.set(self._p & cmd_l, *param_l)


class SYST(COM):
    def __init__(self):
        super(SYST, self).__init__("SYST")


class GEN(COM):
    def __init__(self):
        super(GEN, self).__init__("GEN")


class DEV(COM):
    def __init__(self, address):
        a = "DEV{}".format(address)
        super(DEV, self).__init__(a)


class DEVT(COM):
    def __init__(self,  module_name):
        dt = module_name[:5]
        if dt == "CU4TD":
            t = "TEMD"
        elif dt == "CU4SD":
            t = "SSPD"
        else:
            raise UnsupportedModuleType(self._type)
        super(DEVT, self).__init__(t)


class CU4Messenger(object):
    _ucmd = ["UNKNOWN COMMAND"]
    _errors = ["ERROR: Wrong parameters",
               "ERROR: Timeout"]
    _ok = ["OK"]

    def __init__(self, scpi_serv, attempts=1):
        self._serv = scpi_serv
        self._attempts = attempts
        self._req_failed = None
    
    @property
    def req_failed(self):
        return self._req_failed

    def get(self, cmd_l):
        self._req_failed = True
        resps = [None]
        for attempt in range(0, self._attempts):
            resps = self._serv.get(cmd_l)
            for resp in resps:
                if resp in self._errors:
                    resps = [None]
                    break
                if resp == self._ucmd:
                    raise UnknownCommandException(cmd_l)
            if resps == [None]:
                continue
            else:
                self._req_failed = False
                break
        return resps

    def set(self, cmd_l, *param_l):
        self._req_success = False
        for attempt in range(0, self._attempts):
            resp = self._serv.set(cmd_l, *param_l)
            if resp == self._ok:
                self._req_success = True
                break
            if resp == self._ucmd:
                raise UnknownCommandException((cmd_l, param_l))
        return self._req_success
