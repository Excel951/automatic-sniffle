import serial
import time
from parse_data.utils import retrieve_data as rd

def send_data(port_name, data):
    """Send data to the specified serial port."""
    try:
        with serial.Serial(port=port_name, baudrate=9600, timeout=1) as ser:
            print(f"Connected to {port_name}")
            ser.write(data.encode())  # Send data
            print(f"Data sent: {data}")
            time.sleep(1)  # Give some time for data to be sent

    except serial.SerialException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    PORT_NAME = 'COM1'  # Replace with your port name
    path_file = '../files_hexa/HEXA_EXIAS_20240613_01-19.log.txt'
    # DATA_TO_SEND = 'Hello, Serial Port!'
    DATA_TO_SEND = rd.retrieve_data_read_only(path_file=path_file)
    send_data(PORT_NAME, DATA_TO_SEND)