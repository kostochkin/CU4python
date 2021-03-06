from CU4lib.devices.sd.m0 import CU4SDM0, CU4SDM0Data


class CU4SDM1Data(CU4SDM0Data):
    """ SSPD module Data M1

        See CU4lib.CU4SDM0Data class
    """
    pass


class CU4SDM1(CU4SDM0):
    """ SSPD module M1

        See CU4lib.CU4SDM0 class
    """
    _data_class=CU4SDM1Data
    pass
