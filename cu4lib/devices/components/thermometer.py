from cu4lib.devices.components.descriptors import (
        CU4ComponentContainer,
        CU4BoolValue,
        CU4FloatValue,
        CU4ReadOnly,
        CU4WriteOnly,
        CU4Component
    )
from cu4lib.devices.components.bias import CU4CurrentBias

class CU4Thermometer(CU4ComponentContainer):
    """ CU4Thermometer 
        
        Properties
        ----------
        enabled : bool
            enable/disable thermometer
        temperature : float
            current measured temperature
        bias : CU4CurrentBias
            Bias of the temperature sensor
    """
    enabled = CU4BoolValue("THON")
    temperature = CU4ReadOnly(CU4FloatValue("TEMP"))
    bias = CU4Component(CU4CurrentBias) 


class CU4ThermometerM1(CU4ComponentContainer):
    """ CU4ThermometerM1 
        
        Properties
        ----------
        temperature : float
            current measured temperature
        current : float
            bias current setter
        voltage : float
            bias voltage getter
    """
    temperature = CU4ReadOnly(CU4FloatValue("TEMP"))
    current = CU4WriteOnly(CU4FloatValue("CURR"))
    voltage = CU4ReadOnly(CU4FloatValue("VOLT"))
