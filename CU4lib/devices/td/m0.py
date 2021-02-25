from CU4lib.devices.components.thermometer import CU4Thermometer
from CU4lib.devices.components.pressure import CU4PressureMeter
from CU4lib.devices.components.descriptors import (
        CU4Module,
        CU4Component
    )


class CU4TDM0(CU4Module):
    """ Temperature module M0.
        Base class: CU4Module
        
        Properties
        ----------
        thermometer : CU4Thermometer
            The thermometer component of the module
        pressure_meter : CU4PressureMeter
            The pressure meter component of the module
    """
    thermometer = CU4Component(CU4Thermometer)
    pressure_meter = CU4Component(CU4PressureMeter)
