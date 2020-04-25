import platform
import PySimpleGUI as sg
import just
import struct
from PIL import Image, ImageTk
from io import BytesIO
import base64

sg.theme('LightBlue2')  # Add a touch of color

WIDTH = 60

sofar = sg.Text('', size=(WIDTH, 1), font=('Helvetica', 22, 'underline'))

selected_index = 0

imgs = [
    sg.Image(data=""),
    sg.Image(data=""),
    sg.Image(data=""),
    sg.Image(data=""),
    sg.Image(data=""),
]
inps = [
    sg.Text("Start typing to match emotes!", size=(WIDTH, 1),),
    sg.Text("", size=(WIDTH, 1)),
    sg.Text("Press Escape to exit", size=(WIDTH, 1)),
    sg.Text("Hit Return to choose.", size=(WIDTH, 1)),
    sg.Text("Ctrl-Backspace to empty", size=(WIDTH, 1)),
]

# [sg.Text('_' * (WIDTH + 25))]
layout = [
    [sofar, sg.Button('Ok', visible=False), sg.Button('Cancel', visible=False)],
    [sg.Text('_' * (WIDTH + 25))],
    *[list(x) for x in zip(imgs, inps)],
]

window = sg.Window('emoji-picker', layout, return_keyboard_events=True, font=("Helvetica", 18))

normal_color = sg.theme_text_color()
active_color = sg.theme_input_background_color()

emojis = None

letters = []

cache = {}
matches = []
emoji = ""
last_key = ""


def search():
    global matches
    word = "".join(letters).lower()
    matches = [x for x in emojis if word in x.lower()] or emojis[: len(imgs)]
    for i in range(len(imgs)):
        color = active_color if selected_index == i else None
        if i in range(len(matches)):
            uni, txt, code = matches[i].split("| ")
            if code not in cache:
                cache[code] = just.read(f"~/emoji_picker_images/{code}.base64", unknown_type="txt")
            imgs[i].update(data=cache[code])
        else:
            txt = ""
            imgs[i].update(data="")
        inps[i].update(value=txt, text_color=color)


while True:
    event, values = window.read()
    print(event)
    if emojis is None:
        print("loading emoji")
        emojis = just.read("~/emojis2.txt").split("\n")
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    elif event.startswith("Ok"):
        pass
    elif event.startswith("Control"):
        if last_key.startswith("BackSpace") or event == "\x7f":
            letters = []
            sofar.update(value="".join(letters))
            search()
    elif event.startswith("Shift"):
        pass
    elif event.startswith("Super"):
        pass
    elif event.startswith("Return") or event == "\r":
        emoji = matches[selected_index].split("|")[0]
        break
    elif event.startswith("Escape") or event == "\x1b":
        break
    elif event.startswith("BackSpace") or event == "\x7f":
        if last_key.startswith("Control"):
            letters = []
        else:
            letters = letters[:-1]
        sofar.update(value="".join(letters))
        search()
    elif event.startswith("space") or event == " ":
        letters.append(" ")
        sofar.update(value="".join(letters))
    elif event.startswith("colon") or event == ":":
        letters.append(":")
        sofar.update(value="".join(letters))
    elif event.startswith("semicolon") or event == ";":
        letters.append(";")
        sofar.update(value="".join(letters))
    elif event.startswith("Down") or event == "\uf701":
        selected_index = min(selected_index + 1, min(len(matches), len(imgs)) - 1)
        for i, inp in enumerate(inps):
            color = active_color if selected_index == i else normal_color
            inp.update(text_color=color)
    elif event.startswith("Up") or event == "\uf700":
        selected_index = max(0, selected_index - 1)
        for i, inp in enumerate(inps):
            color = active_color if selected_index == i else normal_color
            inp.update(text_color=color)
    else:
        letter = event.split(":")[0]
        letters.append(letter)
        sofar.update(value="".join(letters))
        selected_index = 0
        search()
    last_key = event

window.close()

if emoji:
    import time
    from pynput.keyboard import Key, Controller
    import pyperclip

    current = pyperclip.paste()

    pyperclip.copy(emoji)

    keyboard = Controller()

    operating_system = platform.system()
    if operating_system == 'Darwin':
        keyboard.press(Key.cmd)
        keyboard.press("v")
        keyboard.release("v")
        keyboard.release(Key.cmd)
    else:
        keyboard.press(Key.ctrl)
        keyboard.press("v")
        keyboard.release("v")
        keyboard.release(Key.ctrl)

    time.sleep(0.1)
    pyperclip.copy(current)
