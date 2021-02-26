class UnsupportedModuleType(Exception):
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
        pl = "{}?\r\n".format(cmd)
        self._t.send(pl)
        return self._process_response()

    def set(self, command_list, param_list):
        cmd = self._cmd(command_list)
        self._t.send(" ".join([cmd] + param_list) + "\r\n")
        return self._process_response()

    def _process_response(self):
        resps = []
        rcvd = ""
        while True:
            rcvd += self._t.receive()
            splt = rcvd.split("\r\n")
            if len(splt) > 1:
                resps += splt[:-1]
                rcvd = splt[-1]
                if rcvd == "":
                    break
        for x in resps:
            if x in self._errors:
                raise SCPIError("{} <{}>".format(resp, pl))
        return resps

    def _cmd(self, command_list):
        return ":".join(command_list)
    

class CU4ModuleServer:
    def __init__(self, scpi_serv, address, dev_type=None):
        self._serv = scpi_serv
        self.bus_address = address
        self._dev = "DEV{}".format(address)
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
            raise UnsupportedModuleType(self._type)

