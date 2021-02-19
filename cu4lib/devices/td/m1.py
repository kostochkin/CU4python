from cu4lib.devices.components.thermometer import CU4ThermometerM1
from cu4lib.devices.components.pressure import CU4PressureMeter
from cu4lib.devices.components.descriptors import (
        CU4Module,
        CU4Component
    )


class CU4TDM1(CU4Module):
    """ Temperature driver M1
        
        Warn: Not tested
        
        Properties
        ----------
        :thermometer0 CU4Thermometer: 1st thermometer component of the module
        :thermometer1 CU4Thermometer: 2nd thermometer component of the module
        :thermometer2 CU4Thermometer: 3th thermometer component of the module
        :thermometer3 CU4Thermometer: 4th thermometer component of the module
    """
    thermometer0 = CU4Component(CU4ThermometerM1, 0)
    thermometer1 = CU4Component(CU4ThermometerM1, 1)
    thermometer2 = CU4Component(CU4ThermometerM1, 2)
    thermometer3 = CU4Component(CU4ThermometerM1, 3)
