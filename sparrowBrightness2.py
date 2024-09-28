import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
import subprocess

class SparrowBrightnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SparrowBrightness")
        # self.root.iconphoto(False, tk.PhotoImage(file=self.resource_path("brightness-icon.png")))
        self.language = self.load_language()
        self.create_widgets()
        self.update_ports()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def load_language(self):
        try:
            with open("language.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return "English"

    def save_language(self, language):
        with open("language.txt", "w") as file:
            file.write(language)

    def create_widgets(self):
        self.language_var = tk.StringVar(value=self.language)
        self.language_menu = ttk.Combobox(self.root, textvariable=self.language_var, values=["English", "Polski"])
        self.language_menu.bind("<<ComboboxSelected>>", self.change_language)
        self.language_menu.pack()

        self.brightness_label = tk.Label(self.root, text=self.get_text("Brightness control"))
        self.brightness_label.pack()

        self.brightness_scale = tk.Scale(self.root, from_=10, to=100, orient="horizontal", command=self.update_brightness)
        self.brightness_scale.pack()

        self.brightness_value_label = tk.Label(self.root, text="{}%".format(self.brightness_scale.get()))
        self.brightness_value_label.pack()

        self.exit_option = tk.BooleanVar(value=True)
        self.exit_checkbox = tk.Checkbutton(self.root, text=self.get_text("Exit on close"), variable=self.exit_option)
        self.exit_checkbox.pack()

    def get_text(self, text):
        translations = {
            "English": {
                "Brightness control": "Brightness control",
                "Exit on close": "Exit on close"
            },
            "Polski": {
                "Brightness control": "Podświetlenie ekranu",
                "Exit on close": "Zamknij przy zamknięciu"
            }
        }
        return translations[self.language].get(text, text)

    def change_language(self, event):
        self.language = self.language_var.get()
        self.save_language(self.language)
        self.brightness_label.config(text=self.get_text("Brightness control"))
        self.exit_checkbox.config(text=self.get_text("Exit on close"))

    def update_brightness(self, value):
        self.brightness_value_label.config(text="{}%".format(value))
        # Here you would add the code to actually change the brightness using xrandr

    def update_ports(self):
        result = subprocess.run(["xrandr"], capture_output=True, text=True)
        lines = result.stdout.split("\n")
        for line in lines:
            if " connected" in line or " disconnected" in line:
                port_name = line.split()[0]
                label = tk.Label(self.root, text=port_name, fg="grey" if "disconnected" in line else "black")
                label.pack()

    def on_closing(self):
        if self.exit_option.get():
            self.root.destroy()
        else:
            self.root.iconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = SparrowBrightnessApp(root)
    root.mainloop()
