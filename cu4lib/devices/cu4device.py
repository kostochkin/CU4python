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
            Use cu4lib.simplelog.StdioLogger implementation as reference.
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

    def data(self):
        """ Fetching all data

        Returns
        _______
        result : Json
        """
        self._logger.debug("Getting data for", self)
        return self._send_command("DATA?")

    def __str__(self):
        """ custom str """
        return "{}:{}:{}".format(self.__class__.__name__, self._cu4server.ip().value(), self._address)
    
    def __repr__(self):
        """ custom repr """
        return self.__str__()

    def _dev_prefix(self):
        p = self.dev_type()
        a = self._address
        return "{}:DEV{}".format(p, a)

    def _send_command(self, cmd):
        return self._cu4server.send_scpi("{}:{}".format(self._dev_prefix(), cmd)).strip()

    def dev_type(self):
        """ SCPI prefix of the device
        Returns
        _______
        prefix : string
        """
        raise UnknownDevice("Device must have prefix")


class CU4DeviceSDM(CU4Device):
    def dev_type(self):
        return "SSPD"


class CU4DeviceTDM(CU4Device):
    def dev_type(self):
        return "TEMD"

    def thermometer(self, enable=None):
        if enable is None:
            return


        return self._send_command("THON 1")

    def set_thermometer_off(self):
        return self._send_command("THON 0")

    def is_thermometer_on(self):
        return self._send_command("THON?") == "1"

