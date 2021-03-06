import json
import sys
from ...servers.scpi import COM
from ..data_storage import Data


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
            setattr(o._components, self._name, self._c_class(o._genserv, o._devserv, o._address, self._channel))
        return getattr(o._components, self._name)

    def __set__(self, o, v):
        raise CU4ComponentError("Can't assign any value to {} {}".format(self.__class__.__name__, self._name))


class CU4String(object):
    _cu4_type = "string"

    def _from_str(self, x):
        return x

    def _to_str(self, x):
        return x

    def __init__(self, cmd):
        self._cmd = cmd
        self._name = None
        self._gen = False
        self.__doc__ = self._cu4_type + " | None "

    def __set_name__(self, o, n):
        self._name = n

    def __get__(self, o, n=None):
        v = self._select_serv(o).get(COM(self._channelize(o)))[0]
        return v and self._from_str(v)

    def __set__(self, o, v):
        self._select_serv(o).set(COM(self._channelize(o)), self._to_str(v))

    def _select_serv(self, o):
        o._lastserv = o._genserv if self._gen else o._devserv
        return o._lastserv


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


class CU4DictValue(CU4String):
    _cu4_type = " dict "

    def _from_str(self, x):
        return json.loads(x)

    def _to_str(self, x):
        return json.dumps(x)


class CU4BoolValue(CU4String):
    _cu4_type = " bool "
    
    def _from_str(self, x):
        return bool(int(x))

    def _to_str(self, x):
        return str(int(x))


class CU4IntValue(CU4String):
    _cu4_type = " int "

    def _from_str(self, x):
        return round(float(x))

    def _to_str(self, x):
        return str(x)


class CU4BitValue(CU4IntValue):
    _cu4_type = " bool "

    def __init__(self, cmd, b):
        super(self.__class__, self).__init__(cmd)
        self._bit = 2**b
        self._nbit = ~self._bit
   
    def __get__(self, o, n=None):
        v = super(self.__class__, self).__get__(o, n) & self._bit
        return v and bool(v & self._bit)

    def __set__(self, o, v):
        v = super(self.__class__, self).__get__(o, None)
        v and self._set_bit(v)

    def _set_bit(self, v):
        if v:
            i |= self._bit
        else:
            i &= self._nbit
        super(self.__class__, self).__set__(o, i)


class CU4FloatValue(CU4String):
    _cu4_type = " float "

    def _from_str(self, x):
        return float(x)

    def _to_str(self, x):
        return str(x)


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


class CU4ComponentContainer(object):
    def __init__(self, genserv, devserv, address, channel=None):
        """ Parameters
            ----------
            scpi_serv : CU4ModuleServer
            action_failed : bool
                Is True if the last action failed

        """
        self._genserv = genserv
        self._devserv = devserv
        self._lastserv = self._genserv
        self._address = address
        self._components = Components()
        self._channel = channel
        if sys.version_info[0] < 3:
            self._set_names_python2()

    @property
    def action_failed(self):
        return self._lastserv.action_failed

    def _set_override_ro(self, name, v):
        for cls in self.__class__.mro():
            vrs = vars(cls)
            if name in vrs:
                vrs[name]._v.__set__(self, v)
                break

    def _set_names_python2(self):
        for cls in self.__class__.mro():
            for v in vars(cls):
                d = cls.__dict__[v]
                if hasattr(d, '__set_name__'):
                    d.__set_name__(self, v)


class CU4Module(CU4ComponentContainer):
    """ Base class for all modules.
        It has some general properties and functions specific to modules.
        
        Properties
        ----------
        data : Data | None
            Receiving all data. Returns corresponding Data object.
        id : str | None
            Device unique id
        last_error : str | None
            Receiving the last error

        Api
        ---
        init() : Bool | None
            Module hardware initialization
        reboot() : Bool | None
            Reboot the module
    """
    id = CU4ReadOnly(CU4Gen(CU4String("DID")))
    last_error = CU4ReadOnly(CU4Gen(CU4String("ERR")))
    _data = CU4ReadOnly(CU4DictValue("DATA"))
    _data_class = Data

    @property
    def data(self):
        d = self._data
        return d and self._data_class(d)

    def init(self):
        """ Module hardware initialization """
        return self._genserv.set(COM("INIT"))
    
    def reboot(self):
        """ Reboot module  """
        return self._genserv.set(COM("BOOT"))
    
    def __str__(self):
        if self.__class__ == CU4Module:
            name = "CU4Unsupported"
        else:
            name = self.__class__.__name__
        return "<{} address={}>".format(
                name,
                self._address)
