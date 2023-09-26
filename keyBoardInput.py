from pynput import keyboard

data = [50] * 5

keys = {
    'w': False,
    'a': False,
    's': False,
    'd': False,
    'q': False,
    'e': False,
    'r': False,
    'f': False,
    'space': False,
    'shift': False
}

def get_move_target_value(key1_pressed, key2_pressed):
    return 50 if key1_pressed and key2_pressed else 100 if key1_pressed else 0 if key2_pressed else 50

def get_power_target_value(value, key1_pressed, key2_pressed):
    return min(value + 5, 100) if key1_pressed else max(value - 5, 0) if key2_pressed else value


def key_action():
    
    data[0] = get_move_target_value(keys['w'],keys['s'])
    data[1] = get_move_target_value(keys['a'],keys['d'])
    data[2] = 0 if keys['space'] else 2 if keys['shift'] else 1
    data[3] = get_power_target_value(data[3],keys['q'],keys['e'])
    data[4] = get_power_target_value(data[4],keys['r'],keys['f'])
     
    print(data, end='\r')
    
    
def process_key(key, key_state):
    try:
        key_name = key.char
        if key_name in keys:
            keys[key_name] = key_state
    except AttributeError:
        if key == keyboard.Key.space:
            keys['space'] = key_state
        elif key == keyboard.Key.shift:
            keys['shift'] = key_state
    key_action()

def on_key_release(key):
    process_key(key, False) 
    

def on_key_press(key): 
    process_key(key, True)




with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()
    





