import time, glob
from subprocess import PIPE, run
import os
import requests
import base64
import time
import shutil
import subprocess
BELOW_NORMAL_PRIORITY_CLASS = 0x00004000

class VideoUploader:
    def __init__(self, mapping, folder = "../touchdesigner/video_output/"):
        self.folder = folder
        self.audiomapping = mapping
        print("create uploader for folder:", folder)

    def loop(self):
        while True:
            try:
                self.uploadFiles()
            except Exception as e:
                print(f"error when uploading {e}")
            time.sleep(1.0)

    def uploadFiles(self):
        start = glob.glob(self.folder+"start_upload*", recursive=False)
        if len(start) < 1:
            return
        os.unlink(self.folder+"start_upload.txt")
        print("upload triggered")
        files = glob.glob(self.folder+"*.mov", recursive=False)
        for file in files:
            #print("start upload", file)
            self.splitFile(file)

    def splitFile(self, file):
        n = os.path.basename(file)
        n = n.replace(".mov", "")

        try:
            output = subprocess.check_output(
                ("reencode_video.bat", n), stderr=subprocess.STDOUT, shell=True, timeout=500,
                universal_newlines=True, creationflags=BELOW_NORMAL_PRIORITY_CLASS)
            print("reencode success")
        except subprocess.CalledProcessError as exc:
            print("Status: FAIL", exc.returncode, exc.output)
        
        try:
            self.processFile(f"../touchdesigner/video_output/upload/{n}.mp4")
        except Exception as e:
            print(f"error uploading {n} {e}")

        #shutil.move(file, f"../touchdesigner/recordings/uploaded/{os.path.basename(file)}")
        os.unlink(file)

    def processFile(self, fileN):
        uuid = os.path.basename(fileN)[:-4]
        start = time.time()
        with open(fileN, "rb") as file:
            print(f"start upload: {os.path.basename(fileN)}")
            url = 'https://upload_url_here'+uuid
            bData = base64.b64encode(file.read())
            x = requests.post(url, bData, auth=('******', '*******'), timeout=500)
            end = time.time()
            duration = end-start
            if x.ok:
                print("Upload complete, took: ", str(duration))
                #os.unlink(fileN)
            else:
                print(f"Upload error: {x.text}")
        #os.unlink(fileN)