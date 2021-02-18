from cu4lib.devices.components.container import CU4ComponentContainer
from cu4lib.devices.components.bias import CU4CurrentBias
from cu4lib.devices.components.comparator import CU4Comparator
from cu4lib.devices.components.counter import CU4Counter
from cu4lib.devices.components.autorecovery import CU4AutoRecovery


class CU4SDM0(CU4ComponentContainer):
    """ SSPD driver M0

        Fields
        ------
        :counts int: get current counts
        :bias CU4DeviceSDM0Bias:
        :comparator CU4DeviceSDM0Comparator:
        :counter CU4DeviceSDM0Counter:
    """
    @CU4ComponentContainer.method("INIT", gen=True)
    def init():
        """ Initialize """
        pass

    @CU4ComponentContainer.component(CU4CurrentBias)
    def bias():
        pass

    @CU4ComponentContainer.component(CU4Comparator)
    def comparator():
        pass

    @CU4ComponentContainer.component(CU4Counter)
    def counter():
        pass

    @CU4ComponentContainer.component(CU4AutoRecovery)
    def auto_recovery():
        pass

