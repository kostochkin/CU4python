from cu4lib.devices.components.descriptors import (
        CU4ComponentContainer,
        CU4FloatValue,
        CU4ReadOnly
    )


class CU4CurrentBias(CU4ComponentContainer):
    """ CU4CurrentBias 
        
        Properties
        ----------
        current : float
            the bias current
        voltage : float
            the bias voltage
    """
    current = CU4FloatValue("CURR")
    voltage = CU4ReadOnly(CU4FloatValue("VOLT"))
