import variable
import threading
from tool import *
import start
from pynput import keyboard
from log_control import *
once = 0

if __name__ == "__main__":
    variable.initialize()


def on_press(key):
    global once
    key = str(key)
    key = key.replace("'", '')

    if key == '\\x01':  # key == ctrl + a
        variable.paused = False
        log_info('start')
        if once == 0:
            once = 1
            thread = threading.Thread(target=start.main)
            thread.start()
    elif key == '\\x02':  # key == ctrl + b
        log_info('stop')
        variable.paused = True


def ready():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


ready()
