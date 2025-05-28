import rtdeState
import csv
import time
import math
import socket
from enum import Enum
import socket
import json
import select

class RuntimeStatus(Enum):
    Stopping = 0
    Stopped = 1
    Running = 2
    Pausing = 3
    Paused = 4
    Resuming = 5
    Offline = -1


class MirrorBot:

    def __init__(self, id, ip, receive_port = 7777, port = 30004) -> None:
        self.id = id
        self.ROBOT_HOST = ip
        self.ROBOT_PORT = port
        self.config_filename = 'rtdeCommand.xml'
        self.ip = ip
        self.q1 = []
        self.q2 = []
        self.q3 = []
        self.q4 = []
        self.q5 = []
        self.q6 = []
        self.filename = ""
        self.cmd = "live"
        self.connected = False
        self.current_state = None

        self.pos_data = None

        self.receive_td_data = False
        self.receive_live_data = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.sock.bind(("127.0.0.1", receive_port))
        self.sock.setblocking(0)

    def loopBot(self, window):
        self.window = window
        while True:
            try:
                self.rtde = rtdeState.RtdeState(self.ROBOT_HOST, self.config_filename, frequency=240)
                while True:
                    try:
                        self.rtde.initialize()
                        break
                    except Exception:
                        print("could not init rtde / retrying in 5 secs")
                        time.sleep(5)
                print(f"{self.ROBOT_HOST}: rtde inited")
                self.connected = True
                lasttime = time.time()
                while True:
                    if self.cmd == "live":
                        #ready = select.select([self.sock], [], [], 1.0)
                        #if ready[0]:
                        #    data = self.sock.recvfrom(1024)
                        #    strdata = data[0].decode("utf-8")
                        #    pos_data = json.loads(strdata.replace('\x00',''))
                        if self.pos_data is not None:
                            self.writeTcp(self.pos_data)
                        self.receiveState()
                        now = time.time()
                        diff = (now-lasttime)*1000
                        lasttime = now
                    if self.cmd == "home":
                        self.writeMode(3)
                        self.receiveState()
            except Exception as e:
                self.connected = False
                print(f"{self.ROBOT_HOST}: Exception in Loop / try reconnect")
                time.sleep(1)

    def loopTd(self, window):
        self.window = window
        while True:
            try:                        
                ready = select.select([self.sock], [], [], 0.5)
                if ready[0]:
                    data = self.sock.recvfrom(1024)
                    strdata = data[0].decode("utf-8")
                    pos_data = json.loads(strdata.replace('\x00',''))
                    self.pos_data = pos_data
                    self.receive_td_data = True
                    if pos_data[3] == 0 and pos_data[4] == 0 and pos_data[5] == 0:
                        self.receive_live_data = False
                    else:
                        self.receive_live_data = True
                else:
                    self.receive_td_data = False
                    self.receive_live_data = False
                time.sleep(0.001)
            except Exception:
                self.receive_td_data = False
                print(f"{self.ROBOT_HOST}: Exception in TD Loop")
                time.sleep(1)

    def writeTcp(self, position):
        self.rtde.set_q.input_double_register_0 = self.clampPosition(position, 0)
        self.rtde.set_q.input_double_register_1 = self.clampPosition(position, 1)
        self.rtde.set_q.input_double_register_2 = self.clampPosition(position, 2)
        self.rtde.set_q.input_double_register_3 = self.clampRotation(position, 3)
        self.rtde.set_q.input_double_register_4 = self.clampRotation(position, 4)
        self.rtde.set_q.input_double_register_5 = self.clampRotation(position, 5)
        self.rtde.set_q.input_double_register_6 = self.clampRotation(position, 6)
        self.writeMode(4)
        self.rtde.con.send(self.rtde.set_q)

    def writeMode(self, new_mode):
        self.rtde.servo.input_int_register_0 = new_mode
        self.rtde.con.send(self.rtde.servo)

    def clampPosition(self, pos, index): # done on bot
        return pos[index]

    def clampRotation(self, pos, index): # done on bot
        return pos[index]

    def receiveState(self):
        self.current_state = self.rtde.receive()

    def stopBot(self):
        self.sendDash(["stop"])

    def sendDash(self, cmds):
        #if self.currentState is None:
        #    return
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                s.connect((self.ip, 29999))
                data = s.recv(1024)
                print(f"Received Dash Response {data!r}")
                for cmd in cmds:
                    #time.sleep(0.15)
                    s.sendall((cmd+"\n").encode())
                    data = s.recv(1024)
                    print(f"Received Dash Response {data!r}")
        except Exception as e:
            print("exception in Dash command")

    def startProgram(self):
        self.sendDash(["load mirror-me.urp", "play"])

    def startHome(self):
        self.cmd = "home"

    def startLive(self):
        self.cmd = "live"
    
    def getStatus(self):
        data = {
            "id": self.id,
            "state": RuntimeStatus.Offline.value,
        }
        if self.current_state is None:
            return data
        
        data["state"] = self.current_state.runtime_state
        return data