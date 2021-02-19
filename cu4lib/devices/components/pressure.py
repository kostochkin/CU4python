from cu4lib.devices.components.descriptors import (
        CU4ComponentContainer,
        CU4FloatValue,
        CU4ReadOnly,
        CU4Component
    )


class CU4PressureMeterVoltage(CU4ComponentContainer):
    """ CU4PressureMeterVoltage
        
        Properties
        ----------
        :positive float: a voltage from the postive pressure sensor contact.
        :negative float: a voltage from the negative pressure sensor contact.
    """
    positive = CU4ReadOnly(CU4FloatValue("PRVP"))
    negative = CU4ReadOnly(CU4FloatValue("PRVN"))


class CU4PressureMeter(CU4ComponentContainer):
    """ CU4PressureMeter
        
        Properties
        ----------
        :pressure float: get current pressure value
        :voltage CU4PressureMeterVoltage: intended to get voltage from sesnor contacts
    """
    pressure = CU4ReadOnly(CU4FloatValue("PRES"))
    voltage = CU4Component(CU4PressureMeterVoltage)
