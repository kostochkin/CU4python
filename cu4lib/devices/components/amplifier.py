from cu4lib.devices.components.descriptors import (
        CU4ComponentContainer,
        CU4BoolValue
    )

class CU4Amplifier(CU4ComponentContainer):
    """ CU4Amplifier
        
        Properties
        ----------
        :enabled bool: enable/disable amplifier
    """
    enabled = CU4BoolValue("AMPE")
