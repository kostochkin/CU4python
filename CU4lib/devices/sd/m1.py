from CU4lib.devices.components.descriptors import (
        CU4Module,
        CU4Component,
        CU4BoolValue,
        CU4DataObject
    )
from ..components.hfbias import CU4CurrentHFBias
from ..components.comparator import CU4Comparator
from ..components.counter import CU4Counter
from ..components.autorecovery import CU4AutoRecovery
from ..components.amplifier import CU4Amplifier
from ..data_storage import Data


class CU4SDM1Data(Data):
    """ SSPD module Data M1

        This class is intended to store data of CU4SDM1.data property.

        See the properties hierarchy of CU4SDM1 for reference.
    """
    def __init__(self, data):
        status = data["Status"]
        hf_enabled = bool(status["HFModeEnable"])
        dicts = {"bias" : {
                    "current": data["CurrentMonitor"] if hf_enabled else data["Current"],
                    "voltage": data["Voltage"],
                    "hf_enabled": hf_enabled},
                 "shorted": bool(status["Shorted"]),
                 "amplifier": {
                    "enabled": bool(status["AmplifierEnable"])},
                 "auto_recovery": {
                    "enabled": bool(status["AutoResetEnable"])},
                 "comparator": {
                    "enabled": bool(status["ComparatorEnable"])},
                 "counter": {
                    "counts": data["Counts"],
                    "enabled": bool(status["CounterEnable"])}}
        super(CU4SDM1Data, self).__init__(dicts)


class CU4SDM1(CU4Module):
    """ SSPD module M1.
        Base class: CU4Module

        Properties
        ----------
        data : CU4SDM1Data | None
            Receiving all data.
        bias : CU4CurrentHFBias
            a CU4CurrentHFBias instance

        comparator : CU4Comparator
            a CU4Comparator instance

        counter : CU4Counter
            a CU4Counter instance

        amplifier : CU4Amplifier
            a CU4Amplifier instance

        shorted : bool | None
            short bias circuit
    """
    bias = CU4Component(CU4CurrentHFBias)
    comparator = CU4Component(CU4Comparator)
    counter = CU4Component(CU4Counter)
    auto_recovery = CU4Component(CU4AutoRecovery)
    amplifier = CU4Component(CU4Amplifier)
    shorted = CU4BoolValue("SHOR")
    data = CU4DataObject(CU4SDM1Data, "DATA")
