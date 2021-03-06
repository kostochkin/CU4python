from CU4lib.devices.components.thermometer import CU4Thermometer
from CU4lib.devices.components.pressure import CU4PressureMeter
from CU4lib.devices.components.descriptors import (
        CU4Module,
        CU4Component
    )
from ..data_storage import Data


class CU4TDM0Data(Data):
    """ Temperature module M0 Data.
        
        This class is intended to store data of CU4TDM0.data property.

        See the properties hierarchy of CU4TDM0 for reference.
    """
    def __init__(self, data):
        dicts = {"thermometer": {
                     "enabled": bool(data["CommutatorOn"]),
                     "temperature": data["Temperature"],
                     "bias": {
                        "current": data["TempSensorCurrent"],
                        "voltage": data["TempSensorVoltage"]}
                     },
                 "pressure_meter": {
                     "pressure": data["Pressure"],
                     "voltage": {
                         "positive": data["PressSensorVoltageP"],
                         "negative": data["PressSensorVoltageN"]
                         }
                     }
                 }
        super(CU4TDM0Data, self).__init__(dicts, self.__class__.__name__)


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
    _data_class = CU4TDM0Data


