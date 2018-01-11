import asyncore
import socket
from concurrent.futures import ThreadPoolExecutor
import asyncio
import multiprocessing


class TcpHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock, callback):
        self.callback = callback
        asyncore.dispatcher_with_send.__init__(self, sock=sock)

    def readable(self):
        return True

    def handle_read(self):
        data = self.recv(1024)
        if len(data) > 0:
            self.callback(data.decode('utf-8'))


def startserver():
    asyncore.loop()


def start_server():
    pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
    loop = asyncio.get_event_loop()
    loop.run_in_executor(pool, startserver)
    loop.close()


class TcpServer(asyncore.dispatcher):
    def __init__(self, host, port, callback):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.callback = callback

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            handler = TcpHandler(sock, self.callback)
