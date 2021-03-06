import socket
from ..simplelog import EmptyLogger


class ErrorCommunicationWithServer(Exception):
    pass


class CU4Server(object):
    def __init__(self, ip, port=9876, logger=None, timeout=3):
        self._ip = ip
        self._port = port
        self._logger = logger or EmptyLogger()
        self._timeout = timeout
        self._modules = None
        self._addr_sock = None

    def _init_socket(self):
        if self._addr_sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self._timeout)
            addr = (self._ip.value, self._port)
            sock.connect(addr)
            self._addr_sock = addr, sock
        return self._addr_sock

    def _close_socket(self):
        _, sock = self._addr_sock
        sock.close()
        self._addr_sock = None

    def send(self, message):
        message = message.encode("ascii")
        self._logger.debug("Sending", message)
        def sender(sock, addr):
            return sock.sendto(message, addr)

        n = self._try_communicate(sender)
        self._logger.debug("Sent", n)
        return n
    
    def receive(self, n=4196):
        def receiver(sock, addr):
            return sock.recv(n)
        
        s = self._try_communicate(receiver, n)
        self._logger.debug("Received ({})".format(len(s)), s)
        return s.decode("ascii")

    def _try_communicate(self, f, *args):
        addrp, sock = self._init_socket()
        try:
            addr, _ = addrp
            self._logger.debug("Communicating with", addr)
            return f(sock, addrp)
        except socket.timeout:
            self._logger.error("Socket timeout")
            self._close_socket()
        raise ErrorCommunicationWithServer(self._ip)

    @property
    def address(self):
        return self._ip
