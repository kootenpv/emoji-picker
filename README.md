# emoji-picker

For any web apps, or pages, like WhatsApp, Slack, Discord and so on this can be used to pick emojis.

## Installation

It's made cross-platform available by relying on `pysimplegui`, `pyperclip` and `pynput`.

It contains the [download_emojis.py](https://github.com/kootenpv/emoji-picker/blob/master/download_emojis.py) script to generate a list of emojis that can be used.

    python -m pip install -r requirements.txt
    python download_emojis.py


### Windows

Please contribute

### OSX

Please contribute

### Linux

The config in i3 is:

    bindsym $mod+i exec --no-startup-id python main.py"

(ensure python refers to the full path and also provide the full path to `main.py`)

Restart i3 and you can call it using `Mod + i` key combo.

![emoji screenshot](./emoji_picker.gif)
