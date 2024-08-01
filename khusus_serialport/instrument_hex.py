import sys
import re

import serial
import time

ENQ = b'\x05'  # ENQUIRY
ACK = b'\x06'  # ACKNOWLEDGE
NAK = b'\x15'  # NOT ACKNOWLEDGE
STX = b'\x02'  # START OF TEXT
ETX = b'\x03'  # END OF TEXT
ETB = b'\x17'  # PERTENGAHAN DATA
CR = b'\x0D'  #
LF = b'\x0A'  # LINE FEED
EOT = b'\x04'  # END OF DATA

class VirtualInstrument:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.flush()

    def send_message(self, message):
        if self.ser.is_open:
            # self.ser.write(message.encode('ascii'))
            self.ser.write(message)
            print(f"Sent: {message}")
        else:
            print("Serial port is not open")

    def receive_message(self):
        # if self.ser.is_open:
        #     response = self.ser.readline().decode('ascii').strip()
        #     print(f"Received: {response}")
        #     return response
        # else:
        #     print("Serial port is not open")
        #     return None
        if self.ser.is_open:
            data = b''
            while True:
                byte = self.ser.read(1)
                print(f"Received: {byte}")
                if not byte:
                    break
                data += byte
                if byte == ETX:
                    break
            return data
        else:
            print("Serial port is not open")
            return None

    def close(self):
        self.ser.close()
        print("Serial port closed")
        sys.exit()

    def receive_data(self):
        init = True
        while True:
            incoming_message = self.receive_message()
            if incoming_message:
                if incoming_message.startswith('<ENQ>') and init:
                    self.send_message('<ACK>')
                    incoming_message = ''
                    init = False
                    # Simulate data transmission
                if incoming_message.startswith('<STX>'):
                    self.send_message('<ACK>')
                    incoming_message = ''
                if incoming_message.startswith('<EOT>'):
                    # self.send_message('<ACK>')
                    self.close()
                    incoming_message = ''
                    # self.send_message('<STX>1...Data...<CR><ETX>xx<CR><LF>')
                    # self.send_message('<EOT>')

    def calculate_checksum(self, data):
        # Menghapus karakter kontrol seperti <STX>, <CR>, <ETX>, dan <LF>
        checksum = 0
        for byte in data:
            checksum = (checksum + byte) % 256
        return checksum

    def send_data(self):
        max_chunk_data = 240 * 2 # doubled because using hex
        dummy = [
            # "H|^&|||Sender^ID|||20240731120000|||||P|1|20240731120000",
            # "P|1|123456||Doe^John||19600101|M|||123 Main St^^Anytown^AN^12345|123-456-7890|||||||||",
            # "P|2|789101|Smith^Jane||19750323|F|||456 Oak St^^Othertown^OT^67890|987-654-3210|||||||||",
            # "O|1|ORD123|TestCode1^TestDescription1^^^|||20240731120000||||||1|||||||F",
            # "O|2|ORD124|TestCode2^TestDescription2^^^|||20240731120000||||||2|||||||F",
            # "O|3|ORD125|TestCode3^TestDescription3^^^|||20240731120000||||||3|||||||F",
            # "L|1|N"
            "H|\^&|||ABX|||||||P|E1394-97|20050111111502"
        ]
        failure_count = 0
        while True:
            self.send_message(ENQ)
            response = self.receive_message()
            if response == ACK:
                break
            failure_count += 1
            if failure_count > 5:
                time.sleep(10)
            else:
                time.sleep(2)
        for index, data in enumerate(dummy):
            # formated_data = f'<STX>{index}{data}<CR><ETX>'
            # formated_data = f'{STX}{index.encode().hex()}{str(data).encode().hex()}{CR}{ETX}'
            # checksum = self.calculate_checksum(formated_data)
            # formated_data += f'{hex(checksum)[2:]}{CR}{LF}5c6e'
            # formated_data += f'{hex(checksum)}<CR><LF>\n'

            # TAMBAHKAN INDEX DI AWAL DATA
            data = str(index+1) + data

            # BUILD DATA UNTUK CARI CHECKSUM DARI DATA + CR + ETX
            data_for_checksum = bytearray(data.encode() + CR + ETX)

            # BUILD DATA MESSAGE
            data = STX.hex() + data.encode().hex() + CR.hex() + ETX.hex()
            # print(f"Hex Data: {data}")
            # print(f"Data for Checksum: {data_for_checksum}")

            # HITUNG CHECKSUM
            checksum = self.calculate_checksum(data_for_checksum)
            # print(f"Checksum: {checksum}")
            # print(f"Hex Checksum: {hex(checksum)[2:]}")

            # BUILD DATA YANG AKAN DIKIRIM
            message = data + hex(checksum)[2:] + CR.hex() + LF.hex()
            # print(f'Message: {message}')

            # MEMBATASI SPY TIDAK LEBIH DARI 240 CHAR
            # chunks = [data[i:i + max_chunk_data] for i in range(0, len(data), max_chunk_data)]
            # for i, chunk in enumerate(chunks):
            #     if i < len(chunks) - 1:
            #         # Send intermediate chunks with <ETB>
            #         message = STX.hex() + chunk + CR.hex() + ETB.hex()
            #     else:
            #         # Send the last chunk with <ETX>
            #         message = STX.hex() + chunk + CR.hex() + ETX.hex()
            #         message += hex(checksum)[2:] + CR.hex() + LF.hex()
            self.send_message(bytes(message.encode()))

            status_reply = False
            while not status_reply:
                response = self.receive_message()
                if response == ACK:
                    status_reply = True

            # self.send_message(formated_data)
        self.send_message(EOT)
        self.close()


if __name__ == "__main__":
    # Gantilah 'COM3' dengan port serial yang sesuai
    instrument = VirtualInstrument('COM1')
    try:
        # instrument.receive_data()
        instrument.send_data()
    except KeyboardInterrupt:
        instrument.close()
        print("Connection closed")
