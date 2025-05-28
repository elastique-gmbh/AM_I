import FreeSimpleGUI as sg
import time
import threading
from mirrorbot import MirrorBot
import platform
import os
import glob
import winsound
from uploader import VideoUploader

from td_interface import TouchDesignerInterface

sg.theme('DarkBlack')

virtualSys = False

botIps = [
    "10.100.100.30"
]


bots = [
    MirrorBot('a', botIps[0], 7777)
]

colData = []
count = 1

for bot in bots:
    id = str(count)
    colData.append(sg.Column([
        [sg.Text(f'Bot {count}')],
        [sg.Text(f'Mode: None', key=f"mode_{id}")],
        [sg.Checkbox('Connected to Bot', default=False, key=f"conn_{id}")],
        [sg.Checkbox('Receiving TD Pos', default=False, key=f"recv_{id}")],
        [sg.Checkbox('Receiving Quest Pos', default=False, key=f"recv_live_{id}")]
    ]))
    count += 1

layout = [ 
    [sg.Button('START PROG', key="start_program_all"), sg.Button('STOP', key="stop")],
    [sg.Button('HOME', key="home_all"), sg.Button('START LIVE', key="live_all")],
    [colData],
    [sg.Output(size=(80,20))]
]

window = sg.Window('elastique - Mirror Me VR', layout, finalize=True)

def startProgram():
    window.write_event_value('start_program_all', '')

td_interface = TouchDesignerInterface(bots, window, startProgram)

def bota_thread(window):
    bots[0].loopBot(window)
threading.Thread(target=bota_thread, args=(window,), daemon=True).start()


def bota_td_thread(window):
    bots[0].loopTd(window)
threading.Thread(target=bota_td_thread, args=(window,), daemon=True).start()

def td_status_thread():
    td_interface.inputLoop()
threading.Thread(target=td_status_thread, args=(), daemon=True).start()

def td_input_thread():
    td_interface.outputLoop()
threading.Thread(target=td_input_thread, args=(), daemon=True).start()

uploader = VideoUploader([])

def uploader_thread():
    uploader.loop()
threading.Thread(target=uploader_thread, args=(), daemon=True).start()

#loadFile(filemapping[0])

while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == "live_all":
        for bot in bots:
            bot.startLive()
    if event == "home_all":
        for bot in bots:
            bot.startHome()
    if event == "start_program_all":
        for bot in bots:
            bot.startProgram()
    if event == "stop":
        for bot in bots:
            bot.stopBot()

    count = 1
    for bot in bots:
        id = str(count)
        if not bot.connected:
            window[f'conn_{id}'].update(background_color="#FF0000")
        else:
            window[f'conn_{id}'].update(background_color="#003B36")
        window[f'conn_{id}'].update(bot.connected)
        window[f'recv_{id}'].update(bot.receive_td_data)
        window[f'mode_{id}'].update(f"Mode: {bot.cmd}")
        if bot.cmd == "live":
            window[f'mode_{id}'].update(background_color="#003B36")
        else:
            window[f'mode_{id}'].update(background_color="#c45f00")
        window[f'recv_live_{id}'].update(bot.receive_live_data)
        count += 1

window.close()