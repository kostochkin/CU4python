from CU4lib.devices.components.descriptors import (
        CU4Module,
        CU4Component,
        CU4BoolValue,
        CU4ReadOnly
    )
from ..components.bias import CU4CurrentBias
from ..components.comparator import CU4Comparator
from ..components.counter import CU4Counter
from ..components.autorecovery import CU4AutoRecovery
from ..components.amplifier import CU4Amplifier
from ..data_storage import Data


class CU4SDM0Data(Data):
    """ SSPD module M0 Data.
        
        This class is intended to store data of CU4SDM0.data property.

        See the properties hierarchy of CU4SDM0 for reference.
    """
    def __init__(self, data):
        status = data["Status"]
        dicts = {"bias": {
                     "current": data["Current"],
                     "voltage": data["Voltage"]},
                 "shorted": bool(status["Shorted"]),
                 "comparator": {
                     "enabled": bool(status["ComparatorEnable"])}, 
                 "counter": {
                     "counts": data["Counts"],
                     "enabled": bool(status["CounterEnable"])},
                 "amplifier": {
                     "enabled": bool(status["AmplifierEnable"])},
                 "auto_recovery": {
                     "enabled": bool(status["AutoResetEnable"])},
                 "is_cmp": bool(status["RfKeyToComparatorEnable"])
                 }
        super(CU4SDM0Data, self).__init__(dicts, self.__class__.__name__)


class CU4SDM0(CU4Module):
    """ SSPD module M0.
        Base class: CU4Module

        Properties
        ----------
        bias : CU4CurrentBias
            a CU4CurrentBias instance

        comparator : CU4Comparator
            a CU4Comparator instance

        counter : CU4Counter
            a CU4Counter instance

        amplifier : CU4Amplifier
            a CU4Amplifier instance

        shorted : bool | None
            short bias circuit

        is_cmp : bool | None
            indicates current output
            

        API
        ---
        switch_to_amp_out() : None
            switches to "AMP" output
        switch_to_cmp_out() : None
            switches to "CMP" output
    """
    bias = CU4Component(CU4CurrentBias)
    comparator = CU4Component(CU4Comparator)
    counter = CU4Component(CU4Counter)
    auto_recovery = CU4Component(CU4AutoRecovery)
    amplifier = CU4Component(CU4Amplifier)
    shorted = CU4BoolValue("SHOR")
    is_cmp = CU4ReadOnly(CU4BoolValue("RFKC"))
    _data_class = CU4SDM0Data

    def switch_to_amp_out(self):
        """ Switching between amp and cmp outputs """
        self._set_override_ro("is_cmp", False)

    def switch_to_cmp_out(self):
        """ Switching between amp and cmp outputs """
        self._set_override_ro("is_cmp", True)
