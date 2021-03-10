from .descriptors import (
        CU4ComponentContainer,
        CU4BoolValue,
        CU4FloatValue,
        CU4ReadOnly,
        CU4WriteOnly,
        CU4Component
    )
from .bias import CU4CurrentBias

class CU4Thermometer(CU4ComponentContainer):
    """ CU4Thermometer 
        
        Properties
        ----------
        enabled : bool | None
            enable/disable thermometer
        temperature : float | None
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
        temperature : float | None
            current measured temperature
        current : float | None
            bias current setter
        voltage : float | None
            bias voltage getter
    """
    temperature = CU4ReadOnly(CU4FloatValue("TEMP"))
    current = CU4WriteOnly(CU4FloatValue("CURR"))
    voltage = CU4ReadOnly(CU4FloatValue("VOLT"))
