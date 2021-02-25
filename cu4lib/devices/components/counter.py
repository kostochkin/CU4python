from cu4lib.devices.components.descriptors import (
        CU4ComponentContainer,
        CU4FloatValue,
        CU4BoolValue,
        CU4ReadOnly,
    )


class CU4Counter(CU4ComponentContainer):
    """ CU4Counter

        Properties
        ----------
        counts : float
            receiving of the number of samples
        enabled : bool
            enable/disable the counter
        time_constant : float
            counter time constant
    """
    counts = CU4ReadOnly(CU4FloatValue("COUN"))
    enabled = CU4BoolValue("COUE")
    time_constant = CU4FloatValue("TIMC")
