import json
from cu4lib.simplelog import StdioLogger


class UnknownDevice(BaseException):
    pass


class CU4Device:
    """Base class for devices"""

    def __init__(self, cu4server, address, logger=StdioLogger()):
        """ CU4Device constructor

        Parameters
        ----------
        :param cu4server : CU4Server
        :param address : int
            address of device on CU4 bus. Can be obtained using SCPI. See manual
        :param logger : Logger
            a logger instance. Any object that have several log functions.
            Use cu4lib.simplelog.StdioLogger implementation as a reference.
        """
        self._cu4server = cu4server
        self._address = address
        self._logger = logger

    def init(self):
        """ Initialize the hardware

        Returns
        -------
        result : bool
        """
        self._logger.debug("Init", self)
        res = self._cu4server.send_scpi("GEN:DEV{}:INIT".format(self._address)).strip()
        self._logger.debug(res)
        return res == "OK"

    @property
    def data(self):
        """ Fetching all data

        Returns
        _______
        result : dict
        """
        self._logger.debug("Getting data for", self)
        return json.loads(self._send_command("DATA?"))

    def dev_type(self):
        """ SCPI prefix of the device
        Returns
        _______
        prefix : string
        """
        raise UnknownDevice("Device must have prefix")

    def __str__(self):
        """ custom str """
        return "{}:{}:{}".format(self.__class__.__name__, self._cu4server.ip().value, self._address)
    
    def __repr__(self):
        """ custom repr """
        return self.__str__()

    def _dev_prefix(self):
        p = self.dev_type()
        a = self._address
        return "{}:DEV{}".format(p, a)

    def _send_command(self, cmd):
        return self._cu4server.send_scpi("{}:{}".format(self._dev_prefix(), cmd)).strip()

    def _get_bool(self, cmd):
        return self._send_command(cmd) == "1"
    
    def _set_bool(self, cmd, value):
        if value:
            val = 1
        else:
            val = 0
        return self._send_command("{} {}".format(cmd, val))

    def _get_float(self, cmd):
        res = self._send_command(cmd)
        try:
            return float(res)
        except ValueError:
            return None

    def _set_float(self, cmd, val):
        return self._send_command("{} {}".format(cmd, val))

    def _get_json(self, cmd):
        res = self._send_command(cmd)
        try:
            return json.loads(res)
        except json.decoder.JSONDecodeError:
            return None
    
    def _set_json(self, cmd, v):
        return self._send_command("{} {}".format(cmd, json.dumps(v)))


class CU4DeviceSDM(CU4Device):
    def dev_type(self):
        return "SSPD"


