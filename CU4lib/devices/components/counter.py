from .descriptors import (
        CU4ComponentContainer,
        CU4FloatValue,
        CU4BoolValue,
        CU4ReadOnly,
    )


class CU4Counter(CU4ComponentContainer):
    """ CU4Counter

        Properties
        ----------
        counts : float | None
            receiving of the number of samples
        enabled : bool | None
            enable/disable the counter
        time_constant : float | None
            counter time constant
    """
    counts = CU4ReadOnly(CU4FloatValue("COUN"))
    enabled = CU4BoolValue("COUE")
    time_constant = CU4FloatValue("TIMC")
