from .descriptors import (
        CU4ComponentContainer,
        CU4FloatValue,
        CU4BoolValue
    )


class CU4Comparator(CU4ComponentContainer):
    """ CU4Comparator

        Properties
        ----------
        enabled : bool | None
            enable/disable the comparator
        level : float | None
            the value of the trigger level for comparator
    """
    enabled = CU4BoolValue("CLE")
    level = CU4FloatValue("CMPR")
