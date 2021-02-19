import json


class CU4ComponentError(Exception):
    pass


class CU4ValueError(Exception):
    pass


class CU4Component:
    def __init__(self, c_class, channel=None):
        self._c_class = c_class
        self._name = None
        self.__doc__ = c_class.__doc__
        self._channel = channel

    def __set_name__(self, o, n):
        self._name = n

    def __get__(self, o, t=None):
        if not hasattr(o._components, self._name):
            setattr(o._components, self._name, self._c_class(o._serv, self._channel))
        return getattr(o._components, self._name)

    def __set__(self, o, v):
        raise CU4ComponentError(f"Can't assign any value to {self.__class__.__name__} {self._name}")


class CU4Value:
    def __init__(self, cmd):
        self._cmd = cmd
        self._name = None
        self._gen = False

    def __set_name__(self, o, n):
        self._name = n

    def __get__(self, o, n=None):
        return o._serv.get([self._channelize(o)], gen=self._gen)

    def __set__(self, o, v):
        o._serv.set([self._channelize(o)], [v], gen=self._gen)

    def _channelize(self, o):
        if o._channel is None:
            return self._cmd
        else:
            return f"{self._cmd}{o._channel}"


class CU4Gen:
    """"""
    def __init__(self, val):
        self._v = val
        self._v._gen = True

    def __set_name__(self, o, n):
        self._v.__set_name__(o, n)

    def __get__(self, o, n=None):
        return self._v.__get__(o, n)

    def __set__(self, o, v):
        self._v.__set__(o, v)


class CU4DictValue(CU4Value):
    """ dict (with JSON repr) """

    def __get__(self, o, n=None):
        return json.loads(super().__get__(o, n))

    def __set__(self, o, v):
        return super().__set__(o, json.dumps(v))


class CU4BoolValue(CU4Value):
    """ bool """

    def __get__(self, o, n=None):
        return bool(int(super().__get__(o, n)))

    def __set__(self, o, v):
        return super().__set__(o, str(int(v)))


class CU4IntValue(CU4Value):
    """ int """

    def __get__(self, o, n=None):
        return round(float(super().__get__(o, n)))

    def __set__(self, o, v):
        return super().__set__(o, str(v))


class CU4BitValue(CU4IntValue):
    """ bit (False/True) """

    def __init__(self, cmd, b):
        super().__init__(cmd)
        self._bit = 2**b
        self._nbit = ~self._bit
   
    def __get__(self, o, n=None):
        return bool(super().__get__(o, n) & self._bit)

    def __set__(self, o, v):
        i = super().__get__(o, None)
        if v:
            i |= self._bit
        else:
            i &= self._nbit
        super().__set__(o, i)


class CU4FloatValue(CU4Value):
    """ float """

    def __get__(self, o, n=None):
        return float(super().__get__(o, n))

    def __set__(self, o, v):
        return super().__set__(o, str(v))


class CU4ReadOnly:
    def __init__(self, value):
        self._v = value
        self.__doc__ = self._v.__doc__ + " (read-only)"

    def __set_name__(self, o, n):
        self._v.__set_name__(o, n)

    def __get__(self, o, n=None):
        return self._v.__get__(o, n)

    def __set__(self, o, v):
        cls_name = self._v.__class__.__name__
        name = self._v._name
        raise CU4ValueError(f"Can't set read only value {cls_name}.{name}")


class CU4WriteOnly:
    def __init__(self, value):
        self._v = value
        self.__doc__ = self._v.__doc__ + " (write-only)"

    def __set_name__(self, o, n):
        self._v.__set_name__(o, n)

    def __get__(self, o, n=None):
        cls_name = self._v.__class__.__name__
        name = self._v._name
        raise CU4ValueError(f"Can't read write only value {cls_name}.{name}")

    def __set__(self, o, v):
        return self._v.__set__(o, v)


class Components:
    pass


class CU4ComponentContainer:
    def __init__(self, scpi_serv, channel=None):
        """ Parameters
            ----------
            :scpi_serv SCPI:
        """
        self._serv = scpi_serv
        self._components = Components()
        self._channel = channel

    def _set_override_ro(self, name, v):
        vars(self.__class__)[name]._v.__set__(self, v)


class CU4Module(CU4ComponentContainer):
    """ General properties
        
        Properties
        ----------
        :data dict:
        :id str:
        :err str"
    """
    data = CU4ReadOnly(CU4DictValue("DATA"))
    id = CU4ReadOnly(CU4Gen(CU4Value("DID")))
    last_error = CU4ReadOnly(CU4Gen(CU4Value("ERR")))


    def init(self):
        """ Module hardware initialization """
        self._serv.set(["INIT"], [], gen=True)
    
    def reboot(self):
        """ Reboot module  """
        self._serv.set(["BOOT"], [], gen=True)
