from cu4lib.devices.components.container import CU4ComponentContainer, FloatValue, BoolValue, IntValue


class CU4Counter(CU4ComponentContainer):
    """ Representing counter

        Properties
        ----------
        :counts int: receiving of the number of samples
        :enabled bool: enable/disable the counter
        :time_constant float: counter time constant
    """

    @CU4ComponentContainer.value("COUN", IntValue)
    def counts():
        """ int: receiving of the number of samples """
        pass

    @CU4ComponentContainer.value("COUE", BoolValue, writable=True)
    def enabled():
        """ bool: enable/disable the counter """
        pass

    @CU4ComponentContainer.value("TIMC", FloatValue, writable=True)
    def time_constant():
        """ float: counter time constant """
        pass
    
