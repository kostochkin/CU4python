from cu4lib.devices.cu4device import CU4Device
from cu4lib.simplelog import StdioLogger


class CU4DeviceTDM(CU4Device):
    """ Temperature driver
        Fields
        ------
        :thermometer Thermometer:
    """
    
    _thermometer = None
    _pressure_meter = None

    def dev_type(self):
        return "TEMD"

    @property
    def thermometer(self):
        if self._thermometer is None:
            self._thermometer = Thermometer(self)
        return self._thermometer
    
    @property
    def pressure_meter(self):
        if self._pressure_meter is None:
            self._pressure_meter = PressureMeter(self)
        return self._pressure_meter


class PressureMeter:
    def __init__(self, cu4device):
        self._cu4device = cu4device

    @property
    def pres(self):
        return self._cu4device._get_float("PRES?")


class Thermometer:
    _bias = None
    
    def __init__(self, cu4device):
        self._cu4device = cu4device

    @property
    def enabled(self):
        return self._cu4device._get_bool("THON?")

    @enabled.setter
    def enabled(self, x):
        return self._cu4device._set_bool("THON", x)

    @property
    def temp(self):
        return self._cu4device._get_float("TEMP?")
    
    @property
    def bias(self):
        if self._bias is None:
            self._bias = ThermometerBias(self._cu4device)
        return self._bias



class ThermometerBias:
    def __init__(self, cu4device):
        self._cu4device = cu4device
    
    @property
    def curr(self):
        return self._cu4device._get_float("CURR?")

    @curr.setter
    def curr(self, n):
        return self._cu4device._set_float("CURR", n)

    @property
    def volt(self):
        return self._cu4device._get_float("VOLT?")


