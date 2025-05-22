import time, glob
from subprocess import PIPE, run
import os
import requests
import base64
import time
import shutil

class BotMover:
    def __init__(self, bot):
        print("start mover")
        self.bot = bot

    def loop(self):
        while True:
            try:
                print("moving")
            except Exception as e:
                print("error when uploading")
            time.sleep(1.0)