import tkinter as tk
import multiprocessing
import pyautogui
from pynput.keyboard import Key, Listener
import time

class Clicker:
    def __init__(self):
        self.x = multiprocessing.Value('i', 1)
        self.status = multiprocessing.Value('i', 0)  # 0 for Offline, 1 for Online
        self.running = multiprocessing.Value('i', 1)  # 1 for running, 0 for stopping

    def create_window(self):
        self.window = tk.Tk()
        self.window.title("Autoclicker")
        self.window.geometry("350x100")

        lbl = tk.Label(self.window, text="Instructions:")
        lbl.grid(column=1, row=1)

        lbl2 = tk.Label(self.window, text="Press the Numlock key to start the autoclicker")
        lbl2.grid(column=1, row=3)

        lbl3 = tk.Label(self.window, text="Press the Numlock key again to stop the autoclicker")
        lbl3.grid(column=1, row=5)

        lbl4 = tk.Label(self.window, text="Status of the autoclicker:")
        lbl4.grid(column=1, row=7)

        self.lbl5 = tk.Label(self.window, text="Offline")
        self.lbl5.grid(column=2, row=7)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.update_status()

    def update_status(self):
        with self.status.get_lock():
            status_text = "Online" if self.status.value == 1 else "Offline"
        self.lbl5.config(text=status_text)
        self.window.after(500, self.update_status)

    def keycheck(self):
        def on_press(key):
            with self.x.get_lock():
                if key == Key.num_lock:
                    self.x.value += 1
                    with self.status.get_lock():
                        self.status.value = 1 if self.x.value % 2 == 0 else 0
            if key == Key.esc:
                return False

        with Listener(on_press=on_press) as listener:
            listener.join()

    def show(self):
        while True:
            with self.running.get_lock():
                if self.running.value == 0:
                    break
            with self.x.get_lock():
                if self.x.value % 2 == 0:
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
            time.sleep(0.1)  # Add a delay to reduce CPU usage

    def on_closing(self):
        with self.running.get_lock():
            self.running.value = 0
        self.window.destroy()

    def run(self):
        self.create_window()
        self.window.mainloop()

if __name__ == '__main__':
    clicker = Clicker()
    app1 = multiprocessing.Process(target=clicker.keycheck)
    app2 = multiprocessing.Process(target=clicker.show)
    app3 = multiprocessing.Process(target=clicker.run)

    app1.start()
    app2.start()
    app3.start()

    app3.join()  # Wait for the window to close
    app1.terminate()
    app2.terminate()
