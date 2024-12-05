import serial
import time
import csv
import matplotlib
matplotlib.use("TkAgg")
import numpy as np
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
import threading

sg.theme('Dark')
latest_weight = None

# Set up serial communication
try:
    ser = serial.Serial('COM4', baudrate=9600, timeout=1)
    ser.flushInput()
    shouldRead = True
except serial.SerialException:
    print('Serial port not found.... Check USB connection', file=sys.stderr)
    shouldRead = False


# Thread function for reading data from the serial port
def readingFunction():
    global ser, latest_weight, shouldRead
    while shouldRead:
        try:
            ser_bytes = ser.readline().decode("utf-8").strip()
            latest_weight = float(ser_bytes)
            print(latest_weight)
        except (serial.SerialException, PermissionError, ValueError) as e:
            print(str(e))
            shouldRead = False
            print('Stopped Reading.... Check USB Connection', file=sys.stderr)


readingThread = threading.Thread(target=readingFunction)
readingThread.start()

# Initialize the plot window and figure
plot_window = 20
y_var = np.zeros(plot_window)

fig, ax = plt.subplots()
line, = ax.plot(y_var)

tare_weight = 0

# Define the PySimpleGUI window layout with an explicit canvas size
layout = [
    [sg.Canvas(key='-CANVAS-', size=(640, 480))],  # Set canvas size
    [sg.Text('Weight: ', key='-WEIGHT_TEXT-', font=('Helvetica', 40)),
     sg.Text('0.0000', key='-WEIGHT_NUMBER-', font=('Helvetica', 40)),
     sg.Text(' Kg', key='-Kg-', font=('Helvetica', 40))],
    [sg.Button('Tare', key='-TARE-', size=(5, 2)), sg.Button('Exit', key='-EXIT-', size=(5, 2))]
]

# Create the window
window = sg.Window('Serial Data Plotter', layout, finalize=True, element_justification='centered')

# Embed Matplotlib plot into PySimpleGUI window
canvas_elem = window['-CANVAS-'].TKCanvas
canvas = FigureCanvasTkAgg(fig, master=canvas_elem)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

# Main event loop
while True:
    event, values = window.read(timeout=100)

    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break

    try:
        if latest_weight is not None:
            # Update tare weight if the Tare button is pressed
            if event == '-TARE-':
                tare_weight = latest_weight

            # Update the displayed weight
            current_weight = latest_weight - tare_weight
            window['-WEIGHT_NUMBER-'].update(f"{current_weight:.4f}")

            # Save the data to a CSV file
            with open("test_data.csv", "a") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow([time.time(), current_weight])

            # Update the plot
            y_var = np.append(y_var[1:], current_weight)
            line.set_ydata(y_var)
            ax.relim()  # Recompute the data limits
            ax.autoscale_view()  # Automatically scale the view
            canvas.draw()  # Redraw the canvas

    except Exception as e:
        print(f"Error: {e}")
        continue

# Stop the reading thread and close the window
shouldRead = False
window.close()
ser.close()
