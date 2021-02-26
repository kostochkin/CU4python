from .host_ip import HostIp
import socket
from .cu4server import CU4Server
from ..simplelog import EmptyLogger


class CU4ServersList:
    """ 
        This class searches servers over an Ethernet.
        It implements the iterator interface, so it can be used in the following way:
        
        .. code-block:: python
            
            from CU4lib import *

            l = CU4ServersList()
            for server in l:
                print(server)
                # Each server represents an CU4 modular system:
                for module in server.modules:
                    print(module)

            # CU4ServersList also support indexing:
            l = CU4ServersList()
            cu_ip = "127.0.0.1"
            # get all modules:
            print(l[cu_ip].modules)
            # get module at address 0:
            print(l[cu_ip][0])
    """
    def __init__(self, host_ip=None, base_port=9876, timeout=3, logger=None):
        self._ip = host_ip or HostIp(logger=logger)
        self._timeout = timeout
        self._base_port = base_port
        self._dict = {}
        self._logger = logger or EmptyLogger()

    def value(self):
        if not self._dict:
            self._enumerate_servers()
        return self._dict

    def __getitem__(self, ip_addr):
        return self.value()[ip_addr]

    def _enumerate_servers(self):
        new_dict = {}
        self._logger.debug("Searching for servers...")
        tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            self._bind_and_listen(tcpsocket)
            self._send_broadcast(udpsocket)
            self._logger.debug("Enumerating...")
            while 1:
                try:
                    new_dict.update(self._incoming_to_servers_dict(tcpsocket))
                except socket.timeout:
                    if not new_dict:
                        # For testing
                        addr = "127.0.0.1"
                        new_dict[addr] = CU4Server(ip=HostIp(addr), port=self._base_port, logger=self._logger)
                        self._logger.warn("Servers not found")
                    break
        finally:
            self._logger.debug("Cleanup")
            tcpsocket.close()
            udpsocket.close()
        self._dict = new_dict
        return self._dict
    
    def _incoming_to_servers_dict(self, tcpsocket):
        conn, adp = tcpsocket.accept()
        data = conn.recv(1024).decode()
        self._logger.debug("Got datagram", data)
        addr, _ = adp
        if addr in data.split(";"):
            self._logger.info("Found server", addr)
            cu4Server = CU4Server(ip=HostIp(addr), port=self._base_port, logger=self._logger)
            return {addr: cu4Server}
        return {}

    def _send_broadcast(self, udpsocket):
        udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udpsocket.settimeout(self._timeout)
        udpsocket.bind(("", self._base_port))
        udpsocket.sendto(self._ip.value.encode(), ('<broadcast>', self._base_port + 1))

    def _bind_and_listen(self, serversocket):
        port = self._base_port + 2
        ip = self._ip.value
        self._logger.debug("Run listener on", ip, ":", port)
        serversocket.bind((ip, port))
        serversocket.listen(5)
        serversocket.settimeout(self._timeout)

    def __iter__(self):
        return iter(self.value().values())

    def __repr__(self):
        a = ", ".join(map(repr, self))
        return "[{}]".format(a)


