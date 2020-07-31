import time
import os
import subprocess
from threading import Thread

# (library) source: https://github.com/boppreh/keyboard
# pip install keyboard
import keyboard


def payload_for_test(squence):
    # open text KDE editor on Linux
    subprocess.Popen(['/usr/bin/kate'])

    for letter in squence:
        keyboard.send(str(letter), do_press=True, do_release=True)


def payload_default():
    # 'C:\Program Files\PreSonus\Studio One 4\\Studio One.exe'
    subprocess.Popen(['C:\Program Files\PreSonus\Studio One 4\\Studio One.exe'])
    keyboard.send('space', do_press=True, do_release=True)


def make_payload():
#    time.sleep(2)
    payload_default()
    # thread = Thread(target = payload_for_test, args = [])
    # thread.start()
    # thread.join()
