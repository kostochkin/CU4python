from CU4lib.devices.components.descriptors import (
        CU4ComponentContainer,
        CU4BoolValue,
        CU4FloatValue,
        CU4IntValue,
        CU4ReadOnly
    )


class CU4AutoRecovery(CU4ComponentContainer):
    """ CU4AutoRecovery
        Bias automatic recovery component
        
        Properties
        ----------
        enabled : bool
            enable/disable component
        threshold : float
            the activation voltage of the auto recovery system
        timeout : float
            the time constant of the auto-recovery system
        counts : int
            the number of automatic recovery system triggers

        API
        ---
        reset_counts() : None
            reset the number of automatic recovery system triggers
    """
    enabled = CU4BoolValue("ARE")
    threshold = CU4FloatValue("ARTH")
    timeout = CU4FloatValue("ARTO")
    counts = CU4ReadOnly(CU4IntValue("ARCO"))

    def reset_counts(self):
        """ reset the number of automatic recovery system triggers """
        self._set_override_ro("counts", 0)
