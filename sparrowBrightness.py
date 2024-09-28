import os
import subprocess
from tkinter import *
from tkinter import ttk

# Lista języków - dodaj tutaj kolejne języki, jak potrzebujesz
LANGUAGES = {"English": "en", "Polski": "pl"}

# Zmienna globalna dla języka
current_language = "en"  # Domyślny język to angielski

# Funkcja do pobierania portów i ich statusów
def get_ports():
    output = subprocess.check_output("xrandr", universal_newlines=True)
    lines = output.splitlines()
    
    ports = {}
    for line in lines:
        if " connected" in line:
            parts = line.split()
            port_name = parts[0]
            status = "active"
            ports[port_name] = status
        elif " disconnected" in line:
            parts = line.split()
            port_name = parts[0]
            status = "inactive"
            ports[port_name] = status
    return ports

# Funkcja do zmiany jasności (szeregowa)
def set_brightness(port, brightness):
    subprocess.call(['xrandr', '--output', port, '--brightness', str(brightness / 100)])

# Ustawienie języka
def set_language(lang_key):
    global current_language
    current_language = LANGUAGES[lang_key]
    update_ui_language()

# Aktualizacja interfejsu użytkownika w zależności od języka
def update_ui_language():
    if current_language == "en":
        root.title("Brightness Control")
        brightness_label.set("Brightness:")
    else:
        root.title("Podświetlenie ekranu")
        brightness_label.set("Podświetlenie:")
    update_port_labels()

# Funkcja do aktualizacji etykiet portów
def update_port_labels():
    for port in ports:
        if ports[port] == "active":
            port_labels[port].config(fg='black')
        else:
            port_labels[port].config(fg='gray')

# Funkcja do aktualizacji jasności
def update_brightness(port, value):
    if value < 5:
        value = 5
    set_brightness(port, value)
    brightness_percentage[port].set(value)

# Tworzenie aplikacji Tkinter
root = Tk()
root.geometry("400x300")
root.minsize(400, 300)
root.resizable(True, True)

# Ustawienia języka
ports = get_ports()
brightness_percentage = {}
port_labels = {}
brightness_sliders = {}

# Etykiety i suwaki dla każdego portu
brightness_label = StringVar()
for port in ports:
    frame = Frame(root)
    frame.pack(pady=5)
    
    port_label = Label(frame, text=port)
    port_label.pack(side=LEFT)
    
    port_labels[port] = port_label

    if ports[port] == "active":
        brightness_percentage[port] = IntVar(value=100)  # Domyślna jasność na 100%
        
        slider = ttk.Scale(frame, from_=5, to=100, variable=brightness_percentage[port], orient='horizontal')
        slider.pack(side=LEFT, padx=5)
        slider.bind("<Motion>", lambda event, p=port: update_brightness(p, brightness_percentage[p].get()))
        brightness_sliders[port] = slider
    else:
        port_label.config(fg='gray')  # Wyłączone porty

# Lista rozwijana do wyboru języka
selected_language = StringVar()
selected_language.set("English")  # Domyślnie język angielski

# Funkcja dla menu języka
language_menu = OptionMenu(root, selected_language, *LANGUAGES.keys(), command=set_language)
language_menu.pack(pady=5)

# Aktualizacja języka przy uruchomieniu
update_ui_language()

# Rozpoczęcie pętli aplikacji
root.mainloop()
