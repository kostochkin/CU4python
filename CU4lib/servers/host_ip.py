import socket
from ..simplelog import EmptyLogger

class HostIp:
    """ 
        It encapsulates or autodetect ip address of the host.
        
        .. code-block:: python
            
            from CU4lib import *

            # Autodetection
            h = HostIp() 
            print(h)
            # Encapsualting
            h = HostIp("123.456.789.101")
            print(h)
    """
    def __init__(self, addr=None, logger=None):
        self._ip = addr
        self._auto = False
        self._logger = logger or EmptyLogger()

    @property
    def value(self):
        if self._ip is None:
            self._ip = self._detect_ip()
        return self._ip
    
    def _detect_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self._logger.debug("Trying to detect my IP address")
            # Any non-localhost address even non-exsiting
            s.connect(('8.8.8.8', 1))
            IP = s.getsockname()[0]
        except Exception:
            self._logger.warn("Failed. Using localhost.")
            IP = '127.0.0.1'
        finally:
            self._logger.debug("Got IP", IP)
            s.close()
        self._auto = True
        return IP

    def __repr__(self):
        v = self.value
        if self._auto:
            a = "Auto"
        else:
            a = "Manual"
        return "<{}IP={}>".format(a, v)

