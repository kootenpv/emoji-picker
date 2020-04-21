import sys
import time
import os

inp = sys.stdin.read(5).strip()

os.system("xclip -selection clipboard -o /tmp/tmpclipboard")
os.system(f'printf "{inp}" | xclip -selection primary')

from pynput.mouse import Button, Controller

mouse = Controller()

mouse.press(Button.middle)
mouse.release(Button.middle)
