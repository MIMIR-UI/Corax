#Version 0.1

import serial
import threading

from config import SERIAL_PORT, BAUD_RATE


radio = serial.Serial(
    port=SERIAL_PORT,
    baudrate=BAUD_RATE,
    timeout=1
)

write_lock = threading.Lock()


# Sends bytes through the radio
def send(data):
    with write_lock:
        radio.write(data + b"\n")
        radio.flush()


# Receives bytes from the radio
def receive():
    data = radio.readline()

    if data:
        return data.rstrip(b"\r\n")

    return None


# Closes the radio connection
def close():
    radio.close()