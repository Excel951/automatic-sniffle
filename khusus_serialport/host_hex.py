import sys

import serial
import time
from parse_data.utils import retrieve_data as rd

ENQ = b'\x05'  # ENQUIRY
ACK = b'\x06'  # ACKNOWLEDGE
NAK = b'\x15'  # NOT ACKNOWLEDGE
STX = b'\x02'  # START OF TEXT
ETX = b'\x03'  # END OF TEXT
ETB = b'\x17'  # PERTENGAHAN DATA
CR = b'\x0D'  #
LF = b'\x0A'  # LINE FEED
EOT = b'\x04'  # END OF DATA


class Host:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.flush()

    def send_message(self, message):
        if self.ser.is_open:
            # self.ser.write(message.encode('ascii'))
            self.ser.write(message)
            print(f'Sent: {message}')
        else:
            print("Serial port is not open")

    def receive_message(self):
        if self.ser.is_open:
            res = self.ser.readline()
            print(f"Received: {res}")
            return res
        else:
            print("Serial port is not open")
            return None
        # if self.ser.is_open:
        #     data = b''
        #     while True:
        #         byte = self.ser.readline()
        #         if not byte:
        #             break
        #         data += byte
        #         if byte.endswith():
        #             break
        #         print(f'{byte}')
        #     print(f"Received: {data}")
        #     return data
        # else:
        #     print("Serial port is not open")
        #     return None

    def close(self):
        self.ser.close()
        print("Serial port closed")
        sys.exit()

    def send_data(self):
        index = 1
        failure_count = 0
        init = True
        while True:
            if init:
                self.send_message('<ENQ>')
            incoming_message = self.receive_message()
            if not incoming_message and failure_count == 6:
                print("Waiting 10 seconds...")
                failure_count = 0
                time.sleep(10)
                init = False
            if not incoming_message:
                print("Waiting 2 second...")
                failure_count += 1
                time.sleep(2)
            else:
                init = False
                if 'ACK' in incoming_message:
                    if index == 2:
                        self.send_message('<STX>2...Data...<CR><ETX>xx<CR><LF>')
                        index += 1
                        incoming_message = ''
                        print(f'Index: {index}')
                    if index == 1:
                        self.send_message('<STX>1...Data...<CR><ETX>xx<CR><LF>')
                        index += 1
                        incoming_message = ''
                        print(f'Index: {index}')
                if 'ACK' in incoming_message:
                    self.send_message('<EOT>')
                    incoming_message = ''
                    print(f'Index: {index}')
                    self.close()

    def receive_data(self):
        init = True
        data = []
        while True:
            incoming_message = self.receive_message()
            if incoming_message:
                print('Incoming message: {}'.format(incoming_message.decode('utf-8')))
                # if incoming_message.startswith('<ENQ>') or incoming_message.startswith(ENQ) and init:
                if incoming_message == ENQ and init:
                    self.send_message(ACK)
                    data.append(incoming_message)
                    incoming_message = ''
                    init = False
                    # Simulate data transmission
                # if incoming_message.startswith('<STX>') or incoming_message.startswith(STX):
                elif incoming_message.decode('utf-8').startswith('02'):
                    self.send_message(ACK)
                    data.append(incoming_message)
                    incoming_message = ''
                # if incoming_message.startswith('<EOT>') or incoming_message.startswith(EOT):
                elif incoming_message == EOT:
                    self.send_message(ACK)
                    data.append(incoming_message)
                    self.close()
                    incoming_message = ''
                    # self.send_message('<STX>1...Data...<CR><ETX>xx<CR><LF>')
                    # self.send_message('<EOT>')

if __name__ == '__main__':
    PORT_NAME = 'COM2'  # Replace with your port name
    # path_file = '../files_hexa/HEXA_EXIAS_20240613_01-19.log.txt'
    # DATA_TO_SEND = 'Hello, Serial Port!'
    # DATA_TO_SEND = rd.retrieve_data_read_only(path_file=path_file)
    # send_data(PORT_NAME, "<ENQ>")
    host = Host(PORT_NAME)
    try:
        # host.send_data()
        host.receive_data()
    except KeyboardInterrupt:
        host.close()
        print("Connection closed")
