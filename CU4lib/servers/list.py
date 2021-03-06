from .host_ip import HostIp
import socket
from .cu4server import CU4Server
from ..simplelog import EmptyLogger
from ..devices.cu4 import CU4
from .scpi import SCPI


class CU4List:
    """ 
        This class implements searching of Control Units in an Ethernet network.

    """
    def __init__(self, host_ip=None, base_port=9876, timeout=1, attempts=3, logger=None):
        """
        Parameters
        ----------

        host_ip : HostIp | None
            An HostIp instance

        base_port : int
            TCP port of Control unit. Default 9876

        timeout : int
            TCP/UDP sockets timeout, default=1

        attempts : int
            The number of attempts to obtain data from modules and search Control Units if no response was received.
            Default=3

        logger : Logger | None
            A logger instance. see CU4Lib.simplelog for reference
        """
        self._ip = host_ip or HostIp(logger=logger)
        self._timeout = timeout
        self._base_port = base_port
        self._dict = {}
        self._logger = logger or EmptyLogger()
        self._attempts = attempts

    def __getitem__(self, ip_addr):
        """
            Parameters
            ----------
            ip_addr : str
                IP address of Control Unit

            Example
            -------
            .. code-block:: python

                from CU4lib import *
    
                culist = CU4List()
                # get CU4 at address 127.0.0.1:
                print(culist["127.0.0.1"])
                # get module at address 0:
                print(culist["127.0.0.1"][0])

        """
        if ip_addr in self._dict:
            return self._dict[ip_addr]
        else:
            serv = CU4Server(ip=HostIp(ip_addr), port=self._base_port, logger=self._logger)
            return CU4(SCPI(serv), attempts=self._attempts)
    
    def __iter__(self):
        """
          Example
          -------
          .. code-block:: python
              
              from CU4lib import *
  
              l = CU4List()
              for cu in l:
                  print(cu)
                  for module in cu:
                      print(module)
        """
        return iter(self._enumerate_servers().values())

    def __repr__(self):
        a = ", ".join(map(repr, self))
        return "[{}]".format(a)

    def _enumerate_step(self, udpsocket, tcpsocket, n):
        self._logger.debug("Enumerating try {}/{}".format(n, self._attempts))
        msg = self._ip.value.encode('ascii')
        self._logger.debug("Sending broadcast", msg)
        udpsocket.sendto(msg, ('<broadcast>', self._base_port + 1))
        while True:
            try:
                ns = self._incoming_to_tuple(tcpsocket)
                if ns is not None:
                    faddr, fserv = ns
                    if faddr not in self._dict:
                        self._logger.info("Found new server", faddr)
                        self._dict[faddr] = fserv
            except socket.timeout:
                if not self._dict:
                    self._logger.warn("Servers not found")
                break

    def _enumerate_servers(self):
        self._dict = {}
        self._logger.debug("Searching for servers...")
        tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._config_broadcast(udpsocket)
        try:
            self._bind_and_listen(tcpsocket)
            for n in range(1, self._attempts + 1):
                self._enumerate_step(udpsocket, tcpsocket, n)
        finally:
            self._logger.debug("Cleanup")
            tcpsocket.close()
            udpsocket.close()
        return self._dict
    
    def _incoming_to_tuple(self, tcpsocket):
        conn, adp = tcpsocket.accept()
        data = conn.recv(1024)
        addr, _ = adp
        self._logger.debug("Got datagram", data, "from server", addr)
        if addr in data.decode("ascii").split(";"):
            cu4Server = CU4Server(ip=HostIp(addr), port=self._base_port, logger=self._logger)
            return addr, CU4(SCPI(cu4Server), attempts=self._attempts)
        return None

    def _config_broadcast(self, udpsocket):
        udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udpsocket.settimeout(self._timeout)
        udpsocket.bind(("", self._base_port))

    def _bind_and_listen(self, serversocket):
        port = self._base_port + 2
        ip = self._ip.value
        self._logger.debug("Run listener on", ip, ":", port)
        serversocket.bind((ip, port))
        serversocket.listen(5)
        serversocket.settimeout(self._timeout)
