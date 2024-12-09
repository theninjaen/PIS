import serial
import threading
import sys
import time

serial_connection = None
should_read = False

MAX_WEIGHT = 30
MAX_UPDATE_INTERVAL = 0.35

weight_adjusted_interval = MAX_UPDATE_INTERVAL
heart_rate = 0.8

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
    global should_read, weight_adjusted_interval, heart_rate
    weight = MAX_WEIGHT
    heart_beat_intervals = [0.8, 0.8, 0.8, 0.8, 0.8]
    last_beat = time.time()

    while should_read:
        try:
            ser_bytes = serial_connection.readline().decode("utf-8").strip()
            ser_bytes = ser_bytes.split()

            weight = float(ser_bytes[1])
            weight = clamp(weight, 0, MAX_WEIGHT)
            weight_adjusted_interval = MAX_UPDATE_INTERVAL - (weight / MAX_WEIGHT * MAX_UPDATE_INTERVAL)

            heart_beat = ser_bytes[3]

            if heart_beat == "1":
                heart_beat_intervals = heart_beat_intervals[1:]
                current_beat = time.time()
                time_since_last_heart_beat = current_beat - last_beat
                heart_beat_intervals.append(time_since_last_heart_beat)
                last_beat = current_beat

                heart_rate = 0

                for interval in heart_beat_intervals:
                    heart_rate += interval

                heart_rate /= len(heart_beat_intervals)

        except (serial.SerialException, PermissionError, ValueError) as e:
            print(str(e))
            should_read = False
            print('Stopped Reading.... Check USB Connection', file=sys.stderr)

def read_weight_adjusted_interval():
    return weight_adjusted_interval

def read_heart_rate():
    return heart_rate

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