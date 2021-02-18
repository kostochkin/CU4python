class UnknownModuleType(Exception):
    pass


class SCPIError(Exception):
    pass


class SCPI:
    _errors = ["UNKNOWN COMMAND",
               "ERROR: Wrong parameters"]

    def __init__(self, transport):
        self._t = transport

    def get(self, command_list):
        cmd = self._cmd(command_list)
        pl = f"{cmd}?\r\n"
        resp = self._t.send_scpi(pl).strip()
        if resp in self._errors:
            raise SCPIError(f"{resp} <{pl}>")
        else:
            return resp

    def set(self, command_list, param_list):
        cmd = self._cmd(command_list)
        prm = self._prm(param_list)
        pl = f"{cmd} {prm}\r\n"
        resp = self._t.send_scpi(pl).strip()
        if resp in self._errors:
            raise SCPIError(f"{resp} <{pl}>")

    def _cmd(self, command_list):
        return ":".join(command_list)
    
    def _prm(self, param_list):
        return " ".join(param_list)


class CU4ModuleServer:
    def __init__(self, scpi_serv, address, dev_type=None):
        self._serv = scpi_serv
        self._dev = f"DEV{address}"
        self._type = CU4ModuleTypePrefix(self, dev_type)
        
    def get(self, cmd_l, gen=False):
        return self._serv.get(self._prefix(gen) + cmd_l)

    def set(self, cmd_l, param_l, gen=False):
        self._serv.set(self._prefix(gen) + cmd_l, param_l)
    
    def _prefix(self, gen):
        return ["GEN" if gen else self._type.prefix, self._dev]


class CU4ModuleTypePrefix:
    def __init__(self, serv, dev_type):
        self._serv = serv
        self._type = dev_type
        self._pref = None

    @property
    def prefix(self):
        self._type = self._type or self._serv.get(["DTYP"], gen=True)
        self._pref = self._pref or self._get_prefix()
        return self._pref
   
    def _get_prefix(self):
        if self._type is None:
            return None
        dt = self._type[:5]
        if dt == "CU4TD":
            return "TEMD"
        elif dt == "CU4SD":
            return "SSPD"
        else:
            raise UnknownModuleType(self._type)

