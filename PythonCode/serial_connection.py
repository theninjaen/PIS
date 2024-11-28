from main import MAX_UPDATE_INTERVAL
import serial
import threading
import sys

serial_connection = None
should_read = False

MAX_WEIGHT = 30

weight_adjusted_interval = MAX_UPDATE_INTERVAL
weight = MAX_WEIGHT

def setup_serial_connection(port, baudrate):
    '''
    Creates a serial connection
    '''
    global should_read, serial_connection

    try:
        serial_connection = serial.Serial(port, baudrate, timeout=1)
        serial_connection.flushInput()
        should_read = True
    except serial.SerialException:
        print('Serial port not found.... Check USB connection', file=sys.stderr)
        should_read = False 
 
def create_arduino_thread():
    '''
    Start the keyboard reading thread
    '''
    arduino_thread = threading.Thread(target=read_arduino)
    arduino_thread.daemon = True
    arduino_thread.start()

def read_arduino():
    global should_read, weight, weight_adjusted_interval

    while should_read:
        try:
            ser_bytes = serial_connection.readline().decode("utf-8").strip()
            weight = float(ser_bytes)
            weight = clamp(weight, 0, MAX_WEIGHT)
            
            weight_adjusted_interval = MAX_UPDATE_INTERVAL - (weight / MAX_WEIGHT * MAX_UPDATE_INTERVAL)
        except (serial.SerialException, PermissionError, ValueError) as e:
            print(str(e))
            should_read = False
            print('Stopped Reading.... Check USB Connection', file=sys.stderr)

def clamp(input, min, max):
    '''
    Returns the input if it is between the min and max values. Returns max value if input is larger,
    returns min value if input is lower
    '''
    if input > max:
        return max
    if input < min:
        return min
    return input