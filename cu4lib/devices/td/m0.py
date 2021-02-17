from cu4lib.devices.cu4device import CU4Device
from cu4lib.simplelog import StdioLogger
from cu4lib.devices.constants import CU4DeviceGeneralConstant, CU4DeviceGeneralConstantCopy


class TemperatureTableException(Exception):
    """ Custom exception """
    pass


class CU4DeviceTDM0(CU4Device):
    """ Temperature driver M0
        Fields
        ------
        :thermometer Thermometer:
        :pressure_meter PressureMeter:
        :constants CU4DeviceTDMConstants:
        :temperature_table TemperatureTable:
    """
    
    _thermometer = None
    _pressure_meter = None
    _constants = None
    _t_table = None

    def dev_type(self):
        return "TEMD"

    @property
    def data(self):
        return CU4DeviceTDM0Data(super().data)

    @property
    def thermometer(self):
        """ :thermometer Thermometer: """
        if self._thermometer is None:
            self._thermometer = Thermometer(self)
        return self._thermometer
    
    @property
    def pressure_meter(self):
        """ :pressure_meter PressureMeter: """
        if self._pressure_meter is None:
            self._pressure_meter = PressureMeter(self)
        return self._pressure_meter

    @property
    def constants(self):
        """ :constants CU4DeviceTDMConstants:
            Warning! Damage is possible. Constants are used to configure the module.
            Do not modify them unless you know what are you doing.
            
            Assignment
            ----------
            :constants_copy CU4DeviceTDMConstantsCopy:
        """
        if self._constants is None:
            self._constants = CU4DeviceTDMConstants(self)
        return self._constants
    
    @constants.setter
    def constants(self, constants_copy):
        self._constants = None
        return self._set_json("EEPR", dict(constants_copy))

    @property
    def temperature_table(self):
        """ :temperature_table TemperatureTable:
            Warning! Damage is possible. Temperature table is a temperature sensor calabration table.
            Do not modify it unless you know what are you doing.

            Assignment
            ----------
            :tbl_copy TemperatureTableCopy:
        """
        if self._t_table is None:
            self._t_table = TemperatureTable(self)
        return self._t_table

    @temperature_table.setter
    def temperature_table(self, tbl_copy):
        if len(tbl_copy) == 100:
            self._t_table = None
            return self._set_json("TEMT", tbl_copy.dict())
        else:
            raise TemperatureTableException("The temperature table must contain exactly 100 points")


class CU4DeviceTDMConstantsCopy:
    """ CU4DeviceTDMConstantsCopy is intended to set all constants of the CU4DeviceTDM atomically.
        Warning! Damage is possible. Constants are used to configure the module.
        Do not modify them unless you know what are you doing.
        
        Using example
        -------------
        Assuming d is a CU4DeviceTDM instance:

        cc = d.constants.copy()
        cc.current_adc.slope = 1
        cc.current_dac.intercept = 100
        d.constants = cc
    """

    def __init__(self, d):
        """ Constructor

            Parameters
            ----------
            :d dict: dict parsed from server response
        """
        self._d = {k: CU4DeviceTDMConstantCopy(d[k], k) for (k, v) in d.items()}

    @property
    def current_adc(self):
        """ :current_adc CU4DeviceTDMConstantCopy: """
        return self._d["Current_ADC"]

    @property
    def current_dac(self):
        """ :current_dac CU4DeviceTDMConstantCopy: """
        return self._d["Current_DAC"]
    
    @property
    def voltage_adc(self):
        """ :voltage_adc CU4DeviceTDMConstantCopy: """
        return self._d["Voltage_ADC"]
    
    @property
    def press_voltage_p_adc(self):
        """ :press_voltage_p_adc CU4DeviceTDMConstantCopy: """
        return self._d["Press_VoltageP_ADC"]
    
    @property
    def press_voltage_n_adc(self):
        """ :press_voltage_n_adc CU4DeviceTDMConstantCopy: """
        return self._d["Press_VoltageN_ADC"]

    def __iter__(self):
        return ((k, v._lst) for (k, v) in self._d.items())
    
    def __repr__(self):
        return str(self._d)


class CU4DeviceTDMConstantCopy(CU4DeviceGeneralConstantCopy):
    pass


class CU4DeviceTDMConstants:
    """ CU4DeviceTDMConstants is intended to get and set any constant instantly """
    def __init__(self, cu4device):
        """ Parameters
            ----------
            :cu4device CU4Device:
        """
        self._cu4device = cu4device

    def copy(self):
        """ Obtain a copy of all constants
        
            Returns
            -------
            :constants CU4DeviceTDMConstantsCopy:
        """
        return CU4DeviceTDMConstantsCopy(self._cu4device._get_json("EEPR?"))
    
    @property
    def current_adc(self):
        """ CU4DeviceTDMConstant
            
            Assignment
            ----------
            :new_c CU4DeviceTDMConstantCopy:
        """
        return CU4DeviceTDMConstant(self._cu4device, "Current_ADC")
    
    @current_adc.setter
    def current_adc(self, new_c):
        a = CU4DeviceTDMConstant(self._cu4device, "Current_ADC")
        a.values_from_copy(new_c)
    
    @property
    def current_dac(self):
        """ CU4DeviceTDMConstant
            
            Assignment
            ----------
            :new_c CU4DeviceTDMConstantCopy:
        """
        return CU4DeviceTDMConstant(self._cu4device, "Current_DAC")
    
    @current_dac.setter
    def current_dac(self, new_c):
        a = CU4DeviceTDMConstant(self._cu4device, "Current_DAC")
        a.values_from_copy(new_c)
    
    @property
    def pressure_voltage_n_adc(self):
        """ CU4DeviceTDMConstant

            Assignment
            ----------
            :new_c CU4DeviceTDMConstantCopy:
        """
        return CU4DeviceTDMConstant(self._cu4device, "Press_VoltageN_ADC")
    
    @pressure_voltage_n_adc.setter
    def pressure_voltage_n_adc(self, new_c):
        a = CU4DeviceTDMConstant(self._cu4device, "Press_VoltageN_ADC")
        a.values_from_copy(new_c)

    @property
    def pressure_voltage_p_adc(self):
        """ CU4DeviceTDMConstant

            Assignment
            ----------
            :new_c CU4DeviceTDMConstantCopy:
        """
        return CU4DeviceTDMConstant(self._cu4device, "Press_VoltageP_ADC")
    
    @pressure_voltage_p_adc.setter
    def pressure_voltage_p_adc(self, new_c):
        a = CU4DeviceTDMConstant(self._cu4device, "Press_VoltageP_ADC")
        a.values_from_copy(new_c)
    
    @property
    def pressure(self):
        """ CU4DeviceTDMConstant """
        return CU4DeviceTDMConstant(self._cu4device, "Pressure")

    def __repr__(self):
        return "<{}(...lazy...)>".format(self.__class__.__name__)


class CU4DeviceTDMConstant(CU4DeviceGeneralConstant):
    def _commands(self, cmd):
        commands = {"Current_ADC": "CADC",
                    "Current_DAC": "CDAC",
                    "Voltage_ADC": "VADC",
                    "Press_VoltageP_ADC": "VPPC",
                    "Press_VoltageN_ADC": "VPNC"}
        return commands[cmd]
    

class PressureMeter:
    _voltage = None

    def __init__(self, cu4device):
        """ Parameters
            ----------
            :cu4device CU4Device:
        """
        self._cu4device = cu4device

    @property
    def pressure(self):
        """ float """
        return self._cu4device._get_float("PRES?")
    
    @property
    def voltage(self):
        """ PressureMeterVoltage """
        if self._voltage is None:
            self._voltage = PressureMeterVoltage(self._cu4device)
        return self._voltage
    

class PressureMeterVoltage:
    def __init__(self, cu4device):
        """ Parameters
            ----------
            :cu4device CU4Device:
        """
        self._cu4device = cu4device

    @property
    def positive(self):
        """ float """
        return self._cu4device._get_float("PRVP?")
    
    @property
    def negative(self):
        """ float """
        return self._cu4device._get_float("PRVN?")


class Thermometer:
    _bias = None
    
    def __init__(self, cu4device):
        """ Parameters
            ----------
            :cu4device CU4Device:
        """
        self._cu4device = cu4device

    @property
    def enabled(self):
        """ bool """
        return self._cu4device._get_bool("THON?")

    @enabled.setter
    def enabled(self, x):
        return self._cu4device._set_bool("THON", x)

    @property
    def temperature(self):
        """ float """
        return self._cu4device._get_float("TEMP?")
    
    @property
    def bias(self):
        """ ThermometerBias """
        if self._bias is None:
            self._bias = ThermometerBias(self._cu4device)
        return self._bias


class ThermometerBias:
    def __init__(self, cu4device):
        """ Parameters
            ----------
            :cu4device CU4Device:
        """
        self._cu4device = cu4device
    
    @property
    def current(self):
        """ float """
        return self._cu4device._get_float("CURR?")

    @current.setter
    def current(self, n):
        return self._cu4device._set_float("CURR", n)

    @property
    def voltage(self):
        """ float """
        return self._cu4device._get_float("VOLT?")


class CU4DeviceTDM0Data:
    """ Contains all data of CU4DeviceTDM0 """
    def __init__(self, dct):
        """ Parameters
            ----------
            :cu4device CU4Device:
        """
        self._dict = dct

    @property
    def commutator_on(self):
        """ int """
        return self._dict["CommutatorOn"]

    @property
    def press_sensor_voltage_n(self):
        """ float """
        return self._dict["PressSensorVoltageN"]

    @property
    def press_sensor_voltage_p(self):
        """ float """
        return self._dict["PressSensorVoltageP"]

    @property
    def pressure(self):
        """ float """
        return self._dict["Pressure"]

    @property
    def temp_sensor_current(self):
        """ float """
        return self._dict["TempSensorCurrent"]

    @property
    def temp_sensor_voltage(self):
        """ float """
        return self._dict["TempSensorVoltage"]

    @property
    def temperature(self):
        """ float """
        return self._dict["Temperature"]

    def __repr__(self):
        return repr(self._dict)


class TemperatureTable:
    """ Temperature table is an iterator that contains TemperaturePoint
        Warning! Damage is possible. Temperature table is a temperature sensor calabration table.
        Do not modify it unless you know what are you doing.
    """

    def __init__(self, cu4device):
        self._cu4device = cu4device

    def copy(self):
        return TemperatureTableCopy(list(self))

    def __iter__(self):
        return iter(map(TemperaturePoint, self._cu4device._get_json("TEMT?")["TempTable"]))


class TemperatureTableCopy:
    """ Temperature table copy is intended to modify the table in module.
        Note that it must contain exactly 100 points.
        Warning! Damage is possible. Temperature table is a temperature sensor calabration table.
        Do not modify it unless you know what are you doing.
    """
    def __init__(self, tbl):
        self._tbl = tbl

    def __iter__(self):
        return iter(self._tbl)

    def dict(self):
        """ Returns
            -------
            dict
        """
        return {"TempTable": list(map(list, sorted(self._tbl, reverse=True)))}

    def __len__(self):
        return len(self._tbl)


class TemperaturePoint:
    """ TemperaturePoint is intended to store temperature table point
        
        Properties
        ----------
        :t int: Temperature
        :v int: Calibaration value at t

    """
    def __init__(self, tpl=None, t=None, v=None):
        self.t = t if tpl is None else tpl[0]
        self.v = v if tpl is None else tpl[1]

    def __repr__(self):
        return "<TPoint(t={},v={})>".format(self.t, self.v)

    def __iter__(self):
        return iter((self.t, self.v))

    def __gt__(self, o):
        return (self.t, self.v) > (o.t, o.v)

