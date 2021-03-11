from ..components.thermometer import CU4ThermometerM1
from ..components.pressure import CU4PressureMeter
from ..components.bias import CU4CurrentBias
from ..components.descriptors import (
        CU4Module,
        CU4Component,
        CU4ComponentContainer,
        CU4ReadOnly,
        CU4DictValue,
        CU4String,
        CU4FloatValue,
        CU4WriteOnly
    )


class CU4TDM1(CU4Module):
    """ Temperature module M1.
        Base class: CU4Module
        
        Properties
        ----------
        current : float (write only)
            Setting of bias currents of all thermometers to desired value
        enabled_25v : bool
            Enables/disables 25V line
        enabled_5v : bool
            Enables/disables 5V line
        thermometer1 : CU4ThermometerM1
            1st thermometer component of the module
        thermometer2 : CU4ThermometerM1
            2nd thermometer component of the module
        thermometer3 : CU4ThermometerM1
            3rd thermometer component of the module
        thermometer4 : CU4ThermometerM1
            4th thermometer component of the module
        temperatures : {1: float, 2: float, 3: float, 4: float}
            Getting of temperatures of all thermometers
        switch_mode : str
            Receiving operating mode of switch
        voltages : {1: float, 2: float, 3: float, 4: float}
            Getting of voltages of all thermometers

        API
        ---
        switch_ac() : None
            Switch to Ac mode
        switch_connect() : None
            Switch to Connected mode
        switch_disconnect() : None
            Switch to Disconnected mode
    """
    thermometer1 = CU4Component(CU4ThermometerM1, 0)
    thermometer2 = CU4Component(CU4ThermometerM1, 1)
    thermometer3 = CU4Component(CU4ThermometerM1, 2)
    thermometer4 = CU4Component(CU4ThermometerM1, 3)
    switch_mode = CU4ReadOnly(CU4String("SMOD"))
    current = CU4WriteOnly(CU4FloatValue("CURR"))
    _volt = CU4ReadOnly(CU4DictValue("VOLT"))
    _temp = CU4ReadOnly(CU4DictValue("TEMP"))
    _rels = CU4ReadOnly(CU4DictValue("RELS"))

    @property
    def voltages(self):
        vs = self._volt
        return {(i+1): vs["U{}".format(i)] for i in range(0,4)}
    
    @property
    def temperatures(self):
        vs = self._temp
        return {(i+1): vs["T{}".format(i)] for i in range(0,4)}

    @property
    def enabled_5v(self):
        return self._rels["5V"]

    @enabled_5v.setter
    def enabled_5v(self, x):
        rels = self._rels
        rels["5V"] = x
        self._set_override_ro("_rels", rels)

    @property
    def enabled_25v(self):
        return self._rels["25V"]

    @enabled_25v.setter
    def enabled_25v(self, x):
        rels = self._rels
        rels["25V"] = x
        self._set_override_ro("_rels", rels)

    def switch_ac(self):
        return self._set_override_ro("switch_mode", "A")
    
    def switch_connect(self):
        return self._set_override_ro("switch_mode", "C")
    
    def switch_disconnect(self):
        return self._set_override_ro("switch_mode", "D")
