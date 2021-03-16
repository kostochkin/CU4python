class Data(object):
    """ Converts dict to a nested object

    Example
    -------

    .. code-block:: python

        >>> o = Data({"a": {"b": {"c": 1, "d": 2}, "e": 3}, "f": 4})
        >>> print(o)
        <Data [a.b.c=1, a.b.d=2, a.e=3, f=4]>
        >>> print(o.a)
        <Data.a [b.c=1, b.d=2, e=3]>
        >>> print(o.a.b)
        <Data.a.b [c=1, d=2]>
        >>> print(o.a.e)
        3
    """
    def __init__(self, dict, path=None):
        self._d = dict
        self._path = path or "Data"

    def __getattr__(self, name):
        if name in self._d:
            o = self._d[name]
            if type(o) is dict:
                return Data(o, "{}.{}".format(self._path, name))
            else:
                return o

    def __repr__(self):
        f = self._flat()
        s = map(lambda d: "{}={}".format(".".join(d[0]), d[1]), f)
        return "<{} [{}]>".format(self._path, ", ".join(s))

    def _flat(self, d=None, pref=[]):
        d = d or self._d
        acc = []
        for k, v in d.items():
            if type(v) == dict:
                acc += self._flat(v, pref + [k])
            else:
                acc.append((pref + [k], v))
        return acc
