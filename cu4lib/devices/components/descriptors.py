import json
import sys


class CU4ComponentError(Exception):
    pass


class CU4ValueError(Exception):
    pass


class CU4Component(object):
    """"""
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
        raise CU4ComponentError("Can't assign any value to {} {}".format(self.__class__.__name__, self._name))


class CU4Value(object):
    _cu4_type = "raw value"

    def __init__(self, cmd):
        self._cmd = cmd
        self._name = None
        self._gen = False
        self.__doc__ = self._cu4_type

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
            return "{}{}".format(self._cmd, o._channel)


class CU4Gen(object):
    def __init__(self, val):
        self._v = val
        self._v._gen = True
        self._cu4_type = val._cu4_type

    def __set_name__(self, o, n):
        self._v.__set_name__(o, n)

    def __get__(self, o, n=None):
        return self._v.__get__(o, n)

    def __set__(self, o, v):
        self._v.__set__(o, v)


class CU4DictValue(CU4Value):
    _cu4_type = " dict (with JSON repr) "

    def __get__(self, o, n=None):
        return json.loads(super(self.__class__, self).__get__(o, n))

    def __set__(self, o, v):
        return super(self.__class__, self).__set__(o, json.dumps(v))


class CU4BoolValue(CU4Value):
    _cu4_type = " bool "

    def __get__(self, o, n=None):
        return bool(int(super(self.__class__, self).__get__(o, n)))

    def __set__(self, o, v):
        return super(self.__class__, self).__set__(o, str(int(v)))


class CU4IntValue(CU4Value):
    _cu4_type = " int "

    def __get__(self, o, n=None):
        return round(float(super(self.__class__, self).__get__(o, n)))

    def __set__(self, o, v):
        return super(self.__class__, self).__set__(o, str(v))


class CU4BitValue(CU4IntValue):
    _cu4_type = " bit (False | True) "

    def __init__(self, cmd, b):
        super(self.__class__, self).__init__(cmd)
        self._bit = 2**b
        self._nbit = ~self._bit
   
    def __get__(self, o, n=None):
        return bool(super(self.__class__, self).__get__(o, n) & self._bit)

    def __set__(self, o, v):
        i = super(self.__class__, self).__get__(o, None)
        if v:
            i |= self._bit
        else:
            i &= self._nbit
        super(self.__class__, self).__set__(o, i)


class CU4FloatValue(CU4Value):
    _cu4_type = " float "

    def __get__(self, o, n=None):
        return float(super(self.__class__, self).__get__(o, n))

    def __set__(self, o, v):
        return super(self.__class__, self).__set__(o, str(v))


class CU4ReadOnly(object):
    def __init__(self, value):
        self._v = value
        self.__doc__ = self._v._cu4_type + " (read-only)"

    def __set_name__(self, o, n):
        self._v.__set_name__(o, n)

    def __get__(self, o, n=None):
        return self._v.__get__(o, n)

    def __set__(self, o, v):
        raise CU4ValueError("Can't set read only value {}.{}".format(
            self._v.__class__.__name__,
            self._v._name))


class CU4WriteOnly(object):
    def __init__(self, value):
        self._v = value
        self.__doc__ = self._v._cu4_type + " (write-only)"

    def __set_name__(self, o, n):
        self._v.__set_name__(o, n)

    def __get__(self, o, n=None):
        raise CU4ValueError("Can't read write only value {}.{}".format(
            self._v.__class__.__name__,
            self._v._name))

    def __set__(self, o, v):
        return self._v.__set__(o, v)


class Components(object):
    pass


def _set_names_python2(self):
    if sys.version_info[0] < 3:
        for v in vars(self.__class__):
            d = self.__class__.__dict__[v]
            if hasattr(d, '__set_name__'):
                d.__set_name__(self, v)


class CU4ComponentContainer(object):
    def __init__(self, scpi_serv, channel=None):
        """ Parameters
            ----------
            :scpi_serv SCPI:
        """
        self._serv = scpi_serv
        self._components = Components()
        self._channel = channel
        _set_names_python2(self)


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
    
    def __str__(self):
        if self.__class__ == CU4Module:
            name = "CU4Unsupported"
        else:
            name = self.__class__.__name__
        return "<{} address={}>".format(
                name,
                self._serv.bus_address)
