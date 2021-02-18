from cu4lib.devices.components.container import CU4ComponentContainer, FloatValue

class CU4CurrentBias(CU4ComponentContainer):
    """ CU4CurrentBias 
        
        Properties
        ----------
        :current float: the bias current
        :voltage float: the bias voltage
    """
    @CU4ComponentContainer.value("CURR", FloatValue, writable=True)
    def current():
        """ :current float: the bias current """
        pass

    @CU4ComponentContainer.value("VOLT", FloatValue)
    def voltage():
        """ :voltage float: the bias voltage """
        pass

