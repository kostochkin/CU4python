from cu4lib.simplelog import StdioLogger

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

