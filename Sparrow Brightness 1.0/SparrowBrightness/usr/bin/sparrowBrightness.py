import os
import subprocess
from tkinter import *
from tkinter import ttk

# Function to get connected and disconnected ports using xrandr
def get_ports():
    """Get the list of active and inactive ports from xrandr command."""
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

# Function to set the brightness of a specific port
def set_brightness(port, brightness):
    """Set the brightness level for a specific port using xrandr."""
    subprocess.call(['xrandr', '--output', port, '--brightness', str(brightness / 100)])

# Function to update the brightness value and apply it
def update_brightness(port, value):
    """Update the brightness value and make sure it's not below 5%."""
    if value < 5:
        value = 5  # Enforce minimum brightness of 5%
    elif value > 100:
        value = 100  # Enforce maximum brightness of 100%
    set_brightness(port, value)
    brightness_percentage[port].set(value)

# Function to increase brightness by 1%
def increase_brightness(port):
    """Increase brightness by 1% for the given port."""
    current_value = brightness_percentage[port].get()
    if current_value < 100:
        update_brightness(port, current_value + 1)

# Function to decrease brightness by 1%
def decrease_brightness(port):
    """Decrease brightness by 1% for the given port."""
    current_value = brightness_percentage[port].get()
    if current_value > 5:
        update_brightness(port, current_value - 1)

# Create the main Tkinter window
root = Tk()
root.geometry("600x300")
root.minsize(600, 300)  # Set minimum window size
root.resizable(True, True)
root.title("Brightness Control")

# Initialize port information
ports = get_ports()
brightness_percentage = {}
port_labels = {}
brightness_sliders = {}

# Create labels and sliders for each port
brightness_label = StringVar()
brightness_label.set("Brightness:")

# Adjust padding and layout
for port in ports:
    frame = Frame(root)
    frame.pack(pady=5, padx=10, fill='x')  # Add horizontal padding for a cleaner look

    # Create a grid for aligning port names, sliders, and buttons
    frame.grid_columnconfigure(0, weight=1)  # First column for port names
    frame.grid_columnconfigure(1, weight=3)  # Second column for sliders
    frame.grid_columnconfigure(2, weight=0)  # Third column for buttons

    # Label for the port name, aligned to the left
    port_label = Label(frame, text=port, anchor='w')
    port_label.grid(row=0, column=0, sticky='w')  # Align the label to the left

    port_labels[port] = port_label

    if ports[port] == "active":
        # Default brightness is set to 100%
        brightness_percentage[port] = IntVar(value=100)

        # Slider to adjust brightness from 5% to 100%, with 150% of the original width
        slider = ttk.Scale(frame, from_=5, to=100, variable=brightness_percentage[port], orient='horizontal', length=300)
        slider.grid(row=0, column=1, padx=5)  # Align the slider to the right with padding
        slider.bind("<Motion>", lambda event, p=port: update_brightness(p, brightness_percentage[p].get()))
        brightness_sliders[port] = slider

        # Add "+" and "-" buttons for increasing and decreasing brightness by 1%
        minus_button = Button(frame, text="-", command=lambda p=port: decrease_brightness(p))
        minus_button.grid(row=0, column=2, padx=5, sticky='e')  # Add button to the right of the slider

        plus_button = Button(frame, text="+", command=lambda p=port: increase_brightness(p))
        plus_button.grid(row=0, column=3, padx=5, sticky='w')  # Add button to the right of the slider
    else:
        port_label.config(fg='gray')  # Gray out inactive ports

# Start the Tkinter main loop
root.mainloop()
