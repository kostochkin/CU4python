from cu4lib.devices.components.container import CU4ComponentContainer, FloatValue
import cu4lib.devices.components.bias as bias


class CU4PressureMeterVoltage(CU4ComponentContainer):
    """ CU4PressureMeterVoltage
        
        Properties
        ----------
        :positive float: a voltage from the postive pressure sensor contact.
        :negative float: a voltage from the negative pressure sensor contact.
    """
    @CU4ComponentContainer.value("PRVP", FloatValue)
    def positive():
        """ float: a voltage from the postive pressure sensor contact. """
        pass
    
    @CU4ComponentContainer.value("PRVN", FloatValue)
    def negative():
        """ float: a voltage from the negative pressure sensor contact. """
        pass


class CU4PressureMeter(CU4ComponentContainer):
    """ CU4PressureMeter
        
        Properties
        ----------
        :pressure float: get current pressure value
        :voltage CU4PressureMeterVoltage: intended to get voltage from sesnor contacts
    """
    @CU4ComponentContainer.value("PRES", FloatValue)
    def pressure(self):
        """ float: get current pressure value """
        pass

    @CU4ComponentContainer.component(CU4PressureMeterVoltage)
    def voltage(self):
        pass
    
