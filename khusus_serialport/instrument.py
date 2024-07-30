import sys

import serial
import time

class VirtualInstrument:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.flush()

    def send_message(self, message):
        if self.ser.is_open:
            self.ser.write(message.encode('ascii'))
            print(f"Sent: {message}")
        else:
            print("Serial port is not open")

    def receive_message(self):
        if self.ser.is_open:
            response = self.ser.readline().decode('ascii').strip()
            print(f"Received: {response}")
            return response
        else:
            print("Serial port is not open")
            return None

    def close(self):
        self.ser.close()

    def run(self):
        while True:
            incoming_message = self.receive_message()
            if incoming_message:
                if incoming_message.startswith('<ENQ>'):
                    self.send_message('<ACK>')
                    incoming_message=''
                    # Simulate data transmission
                if incoming_message.startswith('<STX>'):
                    self.send_message('<ACK>')
                    incoming_message=''
                if incoming_message.startswith('<EOT>'):
                    # self.send_message('<ACK>')
                    self.close()
                    sys.exit()
                    incoming_message=''
                    # self.send_message('<STX>1...Data...<CR><ETX>xx<CR><LF>')
                    # self.send_message('<EOT>')

if __name__ == "__main__":
    # Gantilah 'COM3' dengan port serial yang sesuai
    instrument = VirtualInstrument('COM1')
    try:
        instrument.run()
    except KeyboardInterrupt:
        instrument.close()
        print("Connection closed")
