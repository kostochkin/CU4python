class CU4DeviceGeneralConstant:
    """ CU4DeviceGeneralConstant is intended to get and set the constant instantly
        Warning! Damage is possible. Constants are used to configure the module.
        Do not modify it unless you know what are you doing.
    """

    def __init__(self, cu4server, name):
        self._cu4server = cu4server
        self._name = name
   
    def _commands(self, cmd):
        raise Exception("Must be implemented in child")

    def copy(self):
        """ Returns
            -------
            CU4DeviceGeneralConstantCopy
        """
        return CU4DeviceGeneralConstantCopy(self._getter(), self._name)
        
    def values_from_copy(self, c):
        """ Atomically sets slope and intercept from CU4DeviceGeneralConstantCopy

            Parameters
            ----------
            :c CU4DeviceGeneralConstantCopy :
        """
        self._values_from_list(list(c))

    @property
    def slope(self):
        """ float """
        return self._getter()[0]
    
    @slope.setter
    def slope(self, v):
        return self._setter(0, v)

    @property
    def intercept(self):
        """ float """
        return self._getter()[1]
    
    @intercept.setter
    def intercept(self, v):
        return self._setter(1, v)

    def _getter(self):
        return self._cu4server._get_json(self._commands(self._name) + "?")

    def _setter(self, i, v):
        cur = self._getter()
        cur[i] = v
        return self._values_from_list(cur)

    def _values_from_list(self, lst):
        return self._cu4server._set_json(self._commands(self._name), lst)

    def __repr__(self):
        return "<{}(...lazy...)>".format(self._name)
    

class CU4DeviceGeneralConstantCopy:
    """ CU4DeviceGeneralConstantsCopy is intended to store slope and intercept values of a constant.
        Warning! Damage is possible. Constants are used to configure the module.
        Do not modify it unless you know what are you doing.
        
        Using example
        -------------
        Assuming d is a CU4DeviceXXXX instance:

        cc = d.constants.copy()
        cc.current_adc.slope = 1
        cc.current_adc.intercept = 1
        d.constants = cc
    """

    def __init__(self, lst, name):
        """ Constructor

            Parameters
            ----------
            :lst list: an list got from the corresponding server response
            :name string: constant name in the server response
        """
        self._lst = lst
        self._name = name

    @property
    def slope(self):
        """ :slope float: """
        return self._lst[0]
    
    @slope.setter
    def slope(self, x):
        self._lst[0] = x
    
    @property
    def intercept(self):
        """ :intercept float: """
        return self._lst[1]

    @intercept.setter
    def intercept(self, x):
        self._lst[1] = x
    
    def __repr__(self):
        return "<{}(slope={},intercept={})>".format(self._name, self.slope, self.intercept)

    def __iter__(self):
        return iter(self._lst)

