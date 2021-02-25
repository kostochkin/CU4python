from cu4lib.devices.components.descriptors import (
        CU4Module,
        CU4Component,
        CU4BoolValue,
        CU4ReadOnly
    )
from cu4lib.devices.components.bias import CU4CurrentBias
from cu4lib.devices.components.comparator import CU4Comparator
from cu4lib.devices.components.counter import CU4Counter
from cu4lib.devices.components.autorecovery import CU4AutoRecovery
from cu4lib.devices.components.amplifier import CU4Amplifier


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

        shorted : bool
            short bias circuit

        is_cmp : bool
            indicates current output
            

        API
        ---
        switch_to_amp_out : None
            switches to "AMP" output
        switch_to_cmp_out : None
            switches to "CMP" output
    """
    bias = CU4Component(CU4CurrentBias)
    comparator = CU4Component(CU4Comparator)
    counter = CU4Component(CU4Counter)
    auto_recovery = CU4Component(CU4AutoRecovery)
    amplifier = CU4Component(CU4Amplifier)
    shorted = CU4BoolValue("SHOR")
    is_cmp = CU4ReadOnly(CU4BoolValue("RFKC"))

    def switch_to_amp_out(self):
        """ Switching between amp and cmp outputs """
        self._set_override_ro("is_cmp", False)

    def switch_to_cmp_out(self):
        """ Switching between amp and cmp outputs """
        self._set_override_ro("is_cmp", True)
