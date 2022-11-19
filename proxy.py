import socket
from threading import Thread
import os


class Game2Proxy2Server(Thread):
    def __init__(self, remote_ip, port) -> None:
        super(Game2Proxy2Server, self).__init__()
        self.server2proxy2game: Server2Proxy2Game = None
        self.client_host = None
        self.client_port = None
        self.remote_host = remote_ip
        self.port = port
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind((remote_ip, port))

    def run(self):
        while True:
            data = self.sock.recvfrom(1024)
            self.client_host, self.client_port = data[1]
            print("[client] {}".format(str(data[0])))
            self.server2proxy2game.sock.sendto(data[0], (self.remote_host, self.port))

class Server2Proxy2Game(Thread):
    def __init__(self, local_ip, port):
        super(Server2Proxy2Game, self).__init__()
        self.game2proxy2server: Game2Proxy2Server = None
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind((local_ip, port))

    def run(self):
        while True:
            if((not self.game2proxy2server.client_host) or (not self.game2proxy2server.client_port)):
                continue
            data = self.sock.recvfrom(1024)
            print("[server] {}".format(str(data[0])))
            self.game2proxy2server.sock.sendto(data[0], (self.game2proxy2server.client_host, self.game2proxy2server.client_port))

class Proxy(Thread):
    def __init__(self, local_ip, remote_ip, port):
        super(Proxy, self).__init__()
        self.local_ip = local_ip #Your local ip in the network interface you are going to use
        self.remote_ip = remote_ip #The ip of the game server you want to connect to
        self.port = port # Port of the game the remote server is using

    def run(self):
        print("[proxy({}:{})] setting up".format(self.local_ip, self.port))
        self.game2proxy2server = Game2Proxy2Server(self.remote_ip, self.port)
        self.proxy2server2game = Server2Proxy2Game(self.local_ip, self.port)

        self.game2proxy2server.server2proxy2game = self.proxy2server2game
        self.proxy2server2game.game2proxy2server = self.game2proxy2server

        self.game2proxy2server.start()
        self.proxy2server2game.start()

proxy = Proxy('192.168.18.6', '192.168.18.218', 4444)
proxy.start()

while True:
    try:
        cmd = input('$ ')
        if cmd[:4] == 'quit':
            os._exit(0)
    except Exception as e:
        print(e)