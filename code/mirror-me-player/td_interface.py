import time
import socket
import json
from mirrorbot import MirrorBot
import socket

class TouchDesignerInterface:

    def __init__(self, bots, window, start_prog) -> None:
        self.bots = bots
        self.start_prog = start_prog
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", 7001))

    def inputLoop(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            if addr[0] == "127.0.0.1":
                message = data.decode("utf-8").strip()
                if message.startswith("start_program"):
                    self.start_prog()

    def outputLoop(self):
        while True:
            time.sleep(0.1)
            status = []
            for bot in self.bots:
                status.append(bot.getStatus())
            data = (json.dumps(status)+"\n").encode()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data, ("127.0.0.1", 7000))