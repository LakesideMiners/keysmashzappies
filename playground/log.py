from pynput import keyboard
from threading import Timer


keys_pressed = []


def on_press(key):
    try:
        keys_pressed.append(key.char)
    except AttributeError:
        pass


def on_release(key):
    pass


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as l:
    Timer(5, l.stop).start()
    l.join()
    print("done")



print(keys_pressed)
