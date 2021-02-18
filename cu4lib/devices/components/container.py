import json

class CU4ComponentContainer:
    def __init__(self, scpi_serv):
        self._serv = scpi_serv

    def component(cl):
        def decorator(f):
            name = "_auto" + f.__name__ + "Component"
            @property
            def c(self):
                if not hasattr(self, name):
                    setattr(self, name, cl(self._serv))
                return getattr(self, name)
            c.__doc__ = cl.__doc__
            return c
        return decorator

    def method(command, args=None, gen=False):
        def decorator(f):
            def method(self, *args1):
                return self._serv.set([command], args or args1, gen=gen)
            method.__doc__ = f.__doc__
            return method
        return decorator

    def value(command, val_type, writable=False, fetch_on_set=False, gen=False):
        def decorator(f):
            @property
            def prop(self):
                return val_type.from_str(self._serv.get([command], gen=gen))
            if writable:
                if fetch_on_set:
                    def set(self, x):
                        self._serv.set([command], [val_type.to_str(x, prop.fget(self))], gen=gen)    
                else:
                    def set(self, x):
                        self._serv.set([command], [val_type.to_str(x)], gen=gen)
                prop = prop.setter(set)
            prop.__doc__ = f.__doc__
            return prop
        return decorator


class JsonValue:
    from_str = json.loads
    to_str = json.dumps


class BoolValue:
    from_str = lambda x: bool(int(x))
    to_str = lambda x: str(int(x))


class IntValue:
    from_str = lambda x: int(FloatValue.from_str(x))
    to_str = str


class FloatValue:
    from_str = float
    to_str = str


class BitValue:
    def __init__(self, b):
        self._b = b
    
    def from_str(self, s):
        return bool(int(s) & (2**self._b))

    def to_str(self, f, old):
        d = 2 ** self._b
        if f:
            return old | d
        else:
            return old & (~d)

