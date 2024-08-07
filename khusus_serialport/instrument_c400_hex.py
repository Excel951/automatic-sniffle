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
        #         byte = self.ser.read(1)
        #         print(f"Received: {byte}")
        #         if not byte:
        #             break
        #         data += byte
        #         if byte == ETX:
        #             break
        #     return data
        # else:
        #     print("Serial port is not open")
        #     return None

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
        # DIGUNAKAN UNTUK CHECK PANJANG MESSAGE
        max_chunk_data = 240

        # DUMMY DATA
        dummy = [
            # "H|^&|||Sender^ID|||20240731120000|||||P|1|20240731120000",
            # "P|1|123456||Doe^John||19600101|M|||123 Main St^^Anytown^AN^12345|123-456-7890|||||||||",
            # "P|2|789101|Smith^Jane||19750323|F|||456 Oak St^^Othertown^OT^67890|987-654-3210|||||||||",
            # "O|1|ORD123|TestCode1^TestDescription1^^^|||20240731120000||||||1|||||||F",
            # "O|2|ORD124|TestCode2^TestDescription2^^^|||20240731120000||||||2|||||||F",
            # "O|3|ORD125|TestCode3^TestDescription3^^^|||20240731120000||||||3|||||||F",
            # "L|1|N"
            # "H|\^&|||ABX|||||||P|E1394-97|20050111111502"
                "O|1|2312019||^^^36\^^^37\^^^38\^^^39\^^^40\^^^41\^^^42\^^^43\^^^44\^^^45\^^^46\^^^47\^^^48\^^^49\^^^50\^^^51\^^^52\^^^53\^^^54\^^^55\^^^56\^^^57\^^^58\^^^59\^^^60\^^^61\^^^62\^^^63\^^^64\^^^65\^^^66\^^^67\^^^68\^^^69\^^^70\^^^71\^^^72\^^^73\^^^74|R|19900522105500|||||N||||1"
        ]

        cut_data = []
        for index, data in enumerate(dummy):
            if len(data) > max_chunk_data:
                chunks = [data[i:i + max_chunk_data] for i in range(0, len(data), max_chunk_data)]
                print(f"Print chunks: {chunks}")
                dummy.pop(index)
                cut_data.append(index)
                for i, chunk in enumerate(chunks):
                    dummy.insert(i, chunk)
        print(f"Cut data: {cut_data}")

        # HITUNG JUMLAH KONEKSI GAGAL
        failure_count = 0

        # BUILD INITIAL CONNECTION
        while True:
            # KIRIM PESAN ENQ
            self.send_message(ENQ)
            response = self.receive_message()

            # JIKA PESAN YANG DITERIMA SESUAI
            if response == ACK:
                break

            # HITUNG JUMLAH KONEKSI GAGAL
            failure_count += 1

            # JIKA JUMLAH KONEKSI GAGAL LEBIH DARI 6 KALI
            if failure_count > 5:
                time.sleep(10)
            else:
                time.sleep(2)

        # LOOP DUMMY DATA YANG AKAN DIKIRIM
        for index, data in enumerate(dummy):
            # TAMBAHKAN INDEX DI AWAL DATA
            data = str(index+1) + data

            # BUILD DATA UNTUK CARI CHECKSUM DARI DATA + CR + ETX
            if index in cut_data:
                data_for_checksum = bytearray(data.encode() + ETB)
            else:
                data_for_checksum = bytearray(data.encode() + CR + ETX)

            # BUILD DATA MESSAGE
            if index in cut_data:
                data = STX.hex() + data.encode().hex() + ETB.hex()
            else:
                data = STX.hex() + data.encode().hex() + CR.hex() + ETX.hex()
            print(f"Hex Data: {data}")
            print(f"Data for Checksum: {data_for_checksum}")

            # HITUNG CHECKSUM
            checksum = self.calculate_checksum(data_for_checksum)
            print(f"Checksum: {checksum}")
            print(f"Hex Checksum: {checksum:02x}")
            hex_checksum = f"{checksum:02x}"

            # BUILD DATA YANG AKAN DIKIRIM
            message = data + hex_checksum + CR.hex() + LF.hex()
            # print(f'Message: {message}')
            
            self.send_message(bytes(message.encode()))
            print(f'Message: {message}')

            status_reply = False
            while not status_reply:
                response = self.receive_message()
                if response == ACK:
                    status_reply = True
                elif response == NAK:
                    self.send_message(bytes(message.encode()))

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
