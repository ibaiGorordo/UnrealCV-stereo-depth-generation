import sys
from unrealcv import client
from pynput import keyboard

client.connect()

def _onkeypress(key):
    try: k = key.char # single-char keys
    except: k = key.name # other keys
    #check for quit condition
    if key == keyboard.Key.esc:
        print("LOG INFO: Time to quit")
        return False
    try:
        if k == 'p': #On pressing 'p', capture position.
            pose = client.request('vget /camera/0/pose')
            print("[{}]".format(pose))
            #You can do the rest.
    except:
        pass

def main():
    keyboard_listener = keyboard.Listener(on_press=_onkeypress)
    keyboard_listener.start()
    keyboard_listener.join()
    print("LOG INFO: Quit command completed")

if __name__ == "__main__":
    sys.exit(main())