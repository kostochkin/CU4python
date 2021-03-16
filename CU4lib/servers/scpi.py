class SCPIError(Exception):
    pass


class SCPI:
    """ Encapsulates SCPI requests
    """
    def __init__(self, transport):
        self._t = transport

    @property
    def address(self):
        return self._t.address

    def get(self, command):
        pl = command.query() 
        self._t.send(command.query() + "\r\n")
        return self._process_response()

    def set(self, command, *param_list):
        self._t.send(command.set(*param_list) + "\r\n")
        return self._process_response()

    def _process_response(self):
        resps = []
        rcvd = ""
        while True:
            rcvd += self._t.receive()
            splt = rcvd.split("\r\n")
            if len(splt) > 1:
                resps += splt[:-1]
                rcvd = splt[-1]
                if rcvd == "":
                    break
        return resps


class UnsupportedType(Exception):
    pass


class COM(object):
    """ Encapsulates SCPI Command part

    Constructor params
    ------------------

    cmd : str

    API
    ---
    query() : str
        Returns query command string from current command part

    set(*args : [str]) : str
        Returns set command string from current command part

    & : COM
        Concatenate commands parts

    Example
    -------

    .. code-block:: python

        >>> comA = COM("A")
        >>> comB = COM("B")
        >>> comAB = comA & comB
        >>> print(comAB)
        A:B
        >>> print(comAB.query())
        A:B?
        >>> print(comAB.set("1","2","3"))
        A:B 1,2,3
    """
    def __init__(self, cmd=None):
        if type(cmd) == list:
            self._cmd_l = cmd
        elif type(cmd) == str:
            self._cmd_l = [cmd]
        else:
            raise UnsupportedType("{} : {}".format(cmd, type(cmd).__name__))

    def query(self):
        return str(self) + "?"

    def set(self, *args):
        return "{} {}".format(str(self), ",".join(args))

    def __and__(self, o):
        return COM(self._cmd_l + o._cmd_l) 

    def __str__(self):
        return ":".join(self._cmd_l)
