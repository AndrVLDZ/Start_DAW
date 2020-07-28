import time
import os
import subprocess

# (library) source: https://github.com/boppreh/keyboard
# pip install keyboard
import keyboard

def trigger_keyboard():
    '''Trigger keyboard on machine. Make all keypress'''
    # aka `SPACEBARR.press()`
    keyboard.press('space')

def open_MusicSwissKnife_program():
    '''Open my music editor'''
    # 'C:\Program Files\PreSonus\Studio One 4\\Studio One.exe'
    subprocess.call(['C:\Program Files\PreSonus\Studio One 4\\Studio One.exe'])

def start():
    open_MusicSwissKnife_program()
    trigger_keyboard()
    pass

start()