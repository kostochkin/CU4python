from CU4lib.devices.components.descriptors import (
        CU4ComponentContainer,
        CU4FloatValue,
        CU4BoolValue
    )


class CU4Comparator(CU4ComponentContainer):
    """ CU4Comparator

        Parameters
        ----------
        enabled : bool
            enable/disable the comparator
        level : float
            the value of the trigger level for comparator
    """
    enabled = CU4BoolValue("CLE")
    level = CU4FloatValue("CMPR")
