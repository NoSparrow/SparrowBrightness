import subprocess
import tkinter as tk
from tkinter import ttk
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading

class BrightnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brightness Control")
        self.root.geometry("400x300")

        self.language = 'English'
        self.ports = []

        # Dodanie interfejsu graficznego
        self.create_ui()

        # Zbieranie informacji o portach
        self.update_ports()

    def create_ui(self):
        # Wybór języka
        self.language_label = ttk.Label(self.root, text="Language:")
        self.language_label.pack(pady=5)

        self.language_var = tk.StringVar(value='English')
        self.language_menu = ttk.Combobox(self.root, textvariable=self.language_var, values=['English', 'Polski'])
        self.language_menu.pack(pady=5)
        self.language_menu.bind('<<ComboboxSelected>>', self.change_language)

        # Kontener na porty
        self.ports_frame = ttk.Frame(self.root)
        self.ports_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Przycisk do odświeżenia portów
        self.refresh_button = ttk.Button(self.root, text="Refresh Ports", command=self.update_ports)
        self.refresh_button.pack(pady=10)

    def change_language(self, event=None):
        self.language = self.language_var.get()
        if self.language == 'English':
            self.language_label.config(text="Language:")
            self.refresh_button.config(text="Refresh Ports")
        elif self.language == 'Polski':
            self.language_label.config(text="Język:")
            self.refresh_button.config(text="Odśwież porty")

        self.update_ports()

    def update_ports(self):
        # Czyści poprzednie widżety
        for widget in self.ports_frame.winfo_children():
            widget.destroy()

        # Pobranie informacji z xrandr
        xrandr_output = subprocess.check_output('xrandr').decode('utf-8')
        lines = xrandr_output.split('\n')

        self.ports = []
        for line in lines:
            if ' connected' in line:
                port = line.split()[0]
                active = 'connected' in line and 'disconnected' not in line
                self.ports.append((port, active))

                # Tworzenie interfejsu dla każdego portu
                self.create_port_slider(port, active)

    def create_port_slider(self, port, active):
        port_frame = ttk.Frame(self.ports_frame)
        port_frame.pack(fill=tk.X, pady=5)

        port_label = ttk.Label(port_frame, text=f"{port} ({'Active' if active else 'Inactive'})")
        port_label.pack(side=tk.LEFT, padx=10)

        brightness_slider = ttk.Scale(port_frame, from_=1, to=100, orient=tk.HORIZONTAL, state=tk.NORMAL if active else tk.DISABLED)
        brightness_slider.set(50)  # Domyślna jasność

        # Funkcja do zmiany jasności
        def on_slider_change(event):
            brightness = brightness_slider.get()
            self.set_brightness(port, brightness)

        brightness_slider.bind("<Motion>", on_slider_change)
        brightness_slider.pack(side=tk.RIGHT, padx=10, fill=tk.X, expand=True)

    def set_brightness(self, port, brightness):
        brightness_value = brightness / 100
        subprocess.call(f"xrandr --output {port} --brightness {brightness_value}", shell=True)

    def hide_window(self):
        self.root.withdraw()

    def show_window(self, icon, item):
        self.root.deiconify()

    def quit_app(self, icon, item):
        icon.stop()
        self.root.quit()

# Funkcja tworząca ikonę do tray
def setup_tray(app):
    # Ikona do tray (tworzona dynamicznie)
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 64, 64), fill=(128, 128, 128))

    # Menu tray
    menu = Menu(
        MenuItem('Show', app.show_window),
        MenuItem('Quit', app.quit_app)
    )
    tray_icon = Icon("BrightnessApp", image, "Brightness Control", menu)

    # Uruchamianie tray w osobnym wątku
    tray_thread = threading.Thread(target=tray_icon.run)
    tray_thread.daemon = True
    tray_thread.start()

if __name__ == "__main__":
    root = tk.Tk()

    app = BrightnessApp(root)

    # Ukrycie okna na starcie
    root.withdraw()

    # Konfiguracja tray icon
    setup_tray(app)

    root.mainloop()
