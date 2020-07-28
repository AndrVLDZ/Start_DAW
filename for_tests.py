import subprocess
import keyboard

# def type_letter(letter):
#     keyboard.press(letter)
#     keyboard.release(letter)

# def type_sequence(seq):
#     for letter in seq:
#         type_letter(letter)

# if __name__ == "__main__":
#     # Run programm
#     subprocess.Popen(['C:\Program Files\PreSonus\Studio One 4\\Studio One.exe'])
#     #type_sequence('space')
#     type_letter('space')

class KeyboardSequences():
    def __init__(self):
        self.WIN_PATH = 'C:\Program Files\PreSonus\Studio One 4\\Studio One.exe'

    def default_event(self):
        subprocess.Popen([self.WIN_PATH])
        keyboard.send('space', do_press=True, do_release=True)
    
    def another_cmd(self):
        pass # something

if __name__ == "__main__":
    ks = KeyboardSequences()
    ks.default_event()