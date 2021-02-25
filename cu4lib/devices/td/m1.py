from cu4lib.devices.components.thermometer import CU4ThermometerM1
from cu4lib.devices.components.pressure import CU4PressureMeter
from cu4lib.devices.components.descriptors import (
        CU4Module,
        CU4Component
    )


class CU4TDM1(CU4Module):
    """ Temperature module M1.
        Base class: CU4Module
        
        Warn: tested only with mock
        
        Properties
        ----------
        thermometer1 : CU4ThermometerM1
            1st thermometer component of the module
        thermometer2 : CU4ThermometerM1
            2nd thermometer component of the module
        thermometer3 : CU4ThermometerM1
            3th thermometer component of the module
        thermometer4 : CU4ThermometerM1
            4th thermometer component of the module
    """
    thermometer1 = CU4Component(CU4ThermometerM1, 0)
    thermometer2 = CU4Component(CU4ThermometerM1, 1)
    thermometer3 = CU4Component(CU4ThermometerM1, 2)
    thermometer4 = CU4Component(CU4ThermometerM1, 3)
