from CU4lib.servers.cu4server import CU4Server
import random


random.seed(100500)


class BrokenCU4Server(CU4Server):

    def set_probability(self, p):
        self._prob = p

    def receive(self, n=4196):
        def receiver(sock, addr):
            return sock.recv(n)
        
        s = self._try_communicate(receiver, n)
        self._logger.debug("Received ({})".format(len(s)), s)
        choice = random.uniform(0,1)
        if choice <= self._prob:
            self._logger.debug("Imitate of fail")
            return "ERROR: Timeout\r\n"
        else:
            return s.decode("ascii")
