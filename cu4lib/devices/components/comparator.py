from cu4lib.devices.components.container import CU4ComponentContainer, FloatValue, BoolValue

class CU4Comparator(CU4ComponentContainer):
    """ Representing Comparator
        Parameters
        ----------
        :enabled bool: enable/disable the comparator
        :level float: the value of the trigger level for comparator
    """

    @CU4ComponentContainer.value("CLE", BoolValue, writable=True)
    def enabled():
        """ bool: enable/disable the comparator """
        pass

    @CU4ComponentContainer.value("CMPR", FloatValue, writable=True)
    def level(self):
        """ float: the value of the trigger level for comparator """
        pass

