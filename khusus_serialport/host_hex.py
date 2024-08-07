import sys

import re
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

ENQ_HEX = ENQ.hex()  # ENQUIRY
ACK_HEX = ACK.hex() # ACKNOWLEDGE
NAK_HEX = b'\x15'.hex()  # NOT ACKNOWLEDGE
STX_HEX = b'\x02'.hex()  # START OF TEXT
ETX_HEX = b'\x03'.hex()  # END OF TEXT
ETB_HEX = b'\x17'.hex()  # PERTENGAHAN DATA
CR_HEX = b'\x0D'.hex()  #
LF_HEX = b'\x0A'.hex()  # LINE FEED
EOT_HEX = b'\x04'.hex()  # END OF DATA

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

    def convert_datas_hex(self, hex_strings):
        """
        Fungsi untuk mengubah data dari hex ke string
        :param hex_strings: list: list data dalam bentuk hex
        :return: retrieved_datas: list: list data yang telah diubah ke string
        """
        retrieved_datas = []
        # LOOP DATA YANG TELAH TERKUMPUL
        for hex_string in hex_strings:
            # CONVERT BYTE TO HEX
            temp_message = hex_string.decode('utf-8')
            # CEK JIKA DATA DIAWALI STX
            if temp_message.startswith(STX_HEX):
                # HAPUS STX CR ETX CHECKSUM CR LF
                curr_status_message = temp_message[-8:-6]
                # JIKA DATA YANG DIKIRIM TERPOTONG
                if curr_status_message == ETB_HEX:
                    # HAPUS STX ETB CHECKSUM CR LF
                    cleaned_message = temp_message[2:-8]
                elif curr_status_message == ETX_HEX:
                    # HAPUS STX CR ETX CHECKSUM CR LF
                    cleaned_message = temp_message[2:-10]

                # CONVERT HEX TO STRING
                cleaned_message = bytearray.fromhex(cleaned_message)
                cleaned_message = cleaned_message.decode('utf-8')

                # SIMPAN DATA
                # retrieved_datas.append(self.convert_data_hex(hex_string))
                retrieved_datas.append(cleaned_message)
        return retrieved_datas

    def calculate_checksum(self, data):
        """
        Fungsi untuk menghitung checksum
        :param data: list: data yang akan dihitung checksumnya
        :return: checksum: integer
        """
        checksum = 0
        for byte in data:
            checksum = (checksum + byte) % 256
        return checksum

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
        """
        fungsi untuk terima data dari instrumen
        """

        # VARIABEL UNTUK CEK APAKAH INI KONEKSI YANG PERTAMA KALI
        init = True

        # VARIABEL UNTUK MENYIMPAN SELURUH DATA
        data = []

        while True:
            # TERIMA PESAN YANG DATANG
            incoming_message = self.receive_message()

            # JIKA PESAN TERSEDIA
            if incoming_message:

                # JIKA PESAN YANG DITERIMA ADALAH ENQ
                if incoming_message == ENQ and init:
                    # KIRIM PESAN ACK
                    self.send_message(ACK)
                    # SIMPAN PESAN KE DATA
                    data.append(incoming_message)
                    init = False

                # JIKA PESAN YANG DITERIMA DIAWALI DENGAN STX
                elif incoming_message.decode('utf-8').startswith(STX_HEX):
                    # AMBIL CONTROL MESSAGE SEBELUM CHECKSUM
                    curr_status_message = incoming_message[-8:-6].decode('utf-8')

                    # CEK JIKA DATA YANG DIKIRIM TERPOTONG
                    if curr_status_message == ETB_HEX:
                        will_check = bytearray(self.convert_datas_hex([incoming_message])[0].encode()+ETB)
                    # JIKA DATA TIDAK TERPOTONG
                    elif curr_status_message == ETX_HEX:
                        will_check = bytearray(self.convert_datas_hex([incoming_message])[0].encode()+CR+ETX)

                    # HITUNG CHECKSUM
                    checksum = self.calculate_checksum(will_check)

                    # RETRIEVE CURRENT CHECKSUM
                    current_checksum = incoming_message[-6:-4]
                    # print(f'Current checksum: {current_checksum}')

                    # JIKA CHECKSUM TIDAK COCOK
                    if not bytes(f'{checksum:02x}'.encode()) == current_checksum:
                        # KIRIM PESAN NAK
                        self.send_message(NAK)
                    else:
                        # KIRIM PESAN ACK
                        self.send_message(ACK)
                        # SIMPAN PESAN KE DATA
                        data.append(incoming_message)

                # JIKA PESAN YANG DITERIMA ADALAH EOT
                elif incoming_message == EOT:
                    # self.send_message(ACK)
                    # SIMPAN PESAN KE DATA
                    data.append(incoming_message)
                    print(f'Data array: {data}')

                    init = True

                    # CONVERT DATA FROM HEX
                    datas = self.convert_datas_hex(data)

                    print(f"Datas: {datas}")

                    self.close()

                incoming_message = ''

if __name__ == '__main__':
    PORT_NAME = 'COM2'  # sesuaikan dengan port yang digunakan
    host = Host(PORT_NAME)
    try:
        # host.send_data()
        host.receive_data()
    except KeyboardInterrupt:
        host.close()
        print("Connection closed")
