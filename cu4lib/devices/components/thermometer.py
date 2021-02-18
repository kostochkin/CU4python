from cu4lib.devices.components.container import CU4ComponentContainer, FloatValue, BoolValue
from cu4lib.devices.components.bias import CU4CurrentBias
import cu4lib.devices.components.bias as bias

class CU4Thermometer(CU4ComponentContainer):
    """ CU4Thermometer 
        
        Properties
        ----------
        :enabled bool: enable/disable thermometer
        :temperature float: current measured temperature
        :bias CU4CurrentBias: Bias of the temperature sensor
    """
    @CU4ComponentContainer.value("THON", BoolValue, writable=True)
    def enabled(self):
        """ :enabled bool: enable/disable thermometer """
        pass

    @CU4ComponentContainer.value("TEMP", FloatValue)
    def temperature(self):
        """ :temperature float: current measured temperature"""
        pass
    
    @CU4ComponentContainer.component(CU4CurrentBias)
    def bias():
        pass

