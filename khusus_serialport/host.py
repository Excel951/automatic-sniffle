import sys

import serial
import time
from parse_data.utils import retrieve_data as rd

ENQ = [0x05] # ENQUIRY
ACK = [0x06] # ACKNOWLEDGE
EOT = [0x04] # END OF TEXT
LF = [0x0A] # LINE FEED

class Host:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.flush()

    def send_mssg(self, message):
        if self.ser.is_open:
            self.ser.write(message.encode('ascii'))
            print(f'Sent: {message}')
        else:
            print("Serial port is not open")

    def receive_mssg(self):
        if self.ser.is_open:
            res = self.ser.readline().decode('ascii').strip()
            print(f"Received: {res}")
            return res
        else:
            print("Serial port is not open")
            return None

    def close(self):
        self.ser.close()
        print("Serial port closed")

    def run(self):
        self.send_mssg('<ENQ>')
        index = 1
        while True:
            incoming_message = self.receive_mssg()
            if incoming_message:
                if 'ACK' in incoming_message:
                    if index == 2:
                        self.send_mssg('<STX>2...Data...<CR><ETX>xx<CR><LF>')
                        index += 1
                        incoming_message = ''
                        print(f'Index: {index}')
                    if index == 1:
                        self.send_mssg('<STX>1...Data...<CR><ETX>xx<CR><LF>')
                        index += 1
                        incoming_message = ''
                        print(f'Index: {index}')
                if 'ACK' in incoming_message:
                    self.send_mssg('<EOT>')
                    incoming_message = ''
                    print(f'Index: {index}')
                    self.close()
                    sys.exit()

def send_data(port_name, data):
    """Send data to the specified serial port."""
    try:
        with serial.Serial(port=port_name, baudrate=9600, timeout=1) as ser:
            print(f"Connected to {port_name}")
            ser.write(data.encode())  # Send data
            print(f"Data sent: {data}")
            time.sleep(1)  # Give some time for data to be sent
            # while True:
            #     data_raw = ser.read(ser.in_waiting)
                # if data_raw:
                #     print(f"Data received: {data_raw}")
                # if "<ACK>" or "<ENQ>" or "<EOT>" or data_raw.startswith("<STX>") or data_raw.endswith("<LF>") in data_raw:
                #     ser.write("ACK".encode())
                #     print("Data sent: {}".format("ACK".encode()))

    except serial.SerialException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    PORT_NAME = 'COM2'  # Replace with your port name
    # path_file = '../files_hexa/HEXA_EXIAS_20240613_01-19.log.txt'
    # DATA_TO_SEND = 'Hello, Serial Port!'
    # DATA_TO_SEND = rd.retrieve_data_read_only(path_file=path_file)
    # send_data(PORT_NAME, "<ENQ>")
    host = Host(PORT_NAME)
    try:
        host.run()
    except KeyboardInterrupt:
        host.close()