from cu4lib.devices.components.container import CU4ComponentContainer, FloatValue, BoolValue, IntValue


class CU4AutoRecovery(CU4ComponentContainer):
    """ Bias automatic recovery component
        
        Properties
        ----------
        :enabled bool: enable/disable component
        :threshold float: the activation voltage of the auto recovery system
        :timeaot float: the time constant of the auto-recovery system
        :counts int: the number of automatic recovery system triggers

        API
        ---
        reset_counts() : reset the number of automatic recovery system triggers
    """

    @CU4ComponentContainer.value("ARE", BoolValue, writable=True)
    def enabled():
        """ bool: enable/disable component """
        pass
    
    @CU4ComponentContainer.value("ARTH", FloatValue, writable=True)
    def threshold():
        """ float: the activation voltage of the auto recovery system """
        pass

    @CU4ComponentContainer.value("ARTO", FloatValue, writable=True)
    def timeout():
        """ float: the time constant of the auto-recovery system """
        pass

    @CU4ComponentContainer.value("ARCO", IntValue)
    def counts():
        """ int: the number of automatic recovery system triggers """
        pass

    @CU4ComponentContainer.method("ARCO", ["0"])
    def reset_counts():
        """ reset the number of automatic recovery system triggers """
        pass
