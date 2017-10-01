import socket
import threading
import errno

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    def run(self):
        print('New connection %s:%d' % (self.ip, self.port))
        while True:
            try:
                response = self.clientsocket.recv(4096)
                if response is None or len(response)==0:
                    #client disonnected
                    break
                print('Received: %s' % response)
            except socket.error as e:
                if e.args[0] == errno.EWOULDBLOCK:
                    #timeout error
                    pass
        print('%s:%d disconnected' % (self.ip, self.port))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.settimeout(1.0)
server.bind(('', 9001))
print('Listening on port 9001')
print('CTRL-C to stop server')

try:
    while True:
        try:
            server.listen(1)
            (clientsocket, (ip, port)) = server.accept()
            newthread = ClientThread(ip, port, clientsocket)
            newthread.start()
        except socket.timeout:
            pass
except KeyboardInterrupt:
    pass
    
