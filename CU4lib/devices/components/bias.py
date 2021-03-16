from .descriptors import (
        CU4ComponentContainer,
        CU4FloatValue,
        CU4ReadOnly
    )


class CU4CurrentBias(CU4ComponentContainer):
    """ CU4CurrentBias 
        
        Properties
        ----------
        current : float | None
            the bias current
        voltage : float | None
            the bias voltage
    """
    current = CU4FloatValue("CURR")
    voltage = CU4ReadOnly(CU4FloatValue("VOLT"))
