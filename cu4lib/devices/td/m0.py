from cu4lib.devices.components.thermometer import CU4Thermometer
from cu4lib.devices.components.pressure import CU4PressureMeter
from cu4lib.devices.components.container import CU4ComponentContainer


class CU4TDM0(CU4ComponentContainer):
    """ Temperature driver M0
        
        Properties
        ----------
        :thermometer CU4Thermometer: The thermometer component of the module
        :pressure_meter CU4PressureMeter: The pressure meter component of the module
    """
    @CU4ComponentContainer.method("INIT", gen=True)
    def init():
        """ Initialize """
        pass

    @CU4ComponentContainer.component(CU4Thermometer)
    def thermometer():
        pass
        
    @CU4ComponentContainer.component(CU4PressureMeter)
    def pressure_meter():
        pass
        
