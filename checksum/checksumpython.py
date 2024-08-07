ETX = 0x03
CR = 0x0D
import re
def calculate_checksum(data):
    checksum = 0
    for byte in data:
        print(f'Byte: {byte}')
        checksum = (checksum + byte) % 256
    return checksum

a = "334f7c317c323331323031397c7c5e5e5e33365c5e5e5e33375c5e5e5e33385c5e5e5e33395c5e5e5e34305c5e5e5e34315c5e5e5e34325c5e5e5e34335c5e5e5e34345c5e5e5e34355c5e5e5e34365c5e5e5e34375c5e5e5e34385c5e5e5e34395c5e5e5e35305c5e5e5e35315c5e5e5e35325c5e5e5e35335c5e5e5e35345c5e5e5e35355c5e5e5e35365c5e5e5e35375c5e5e5e35385c5e5e5e35395c5e5e5e36305c5e5e5e36315c5e5e5e36325c5e5e5e36335c5e5e5e36345c5e5e5e36355c5e5e5e36365c5e5e5e36375c5e5e5e36385c5e5e5e36395c5e5e5e37305c5e5e5e37315c5e5e5e37325c5e5e5e373317"
# HAPUS CHAR YANG TIDAK DIPERLUKAN
pattern_hexa = r'[0x]*([\w+\d+]{2})'

# BERSIHKAN HEXA DARI 0x YANG TIDAK DIPERLUKAN
hexa_cleaned = re.findall(pattern=pattern_hexa, string=a)

# GABUNGKAN HEX YANG TELAH BERSIH DALAM SATU VARIABEL
hexa_string = " ".join(hexa_cleaned)

# CONVERT DATA DARI HEX
result = bytearray.fromhex(hexa_string)
# result = str(result)
# result = result.decode("utf-8")
data = bytearray([0x31, 0x48, 0x7C, 0x5C, 0x5E, 0x26, 0x7C, 0x7C, 0x7C, 0x41, 0x42, 0x58, 0x7C, 0x7C, 0x7C, 0x7C, 0x7C, 0x7C, 0x7C, 0x50, 0x7C, 0x45, 0x31, 0x33, 0x39, 0x34, 0x2D, 0x39, 0x37, 0x7C, 0x32, 0x30, 0x30, 0x35, 0x30, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x35, 0x30, 0x32, 0x0d, 0x03])
print(f"Data: {result}")
checksum = calculate_checksum(result)
print(f"Checksum Desimal: {checksum}")
print(f"Checksum Hexadecimal: 0x{checksum:02x}")

tes = "H|\^&|||ABX|||||||P|E1394-97|20050111111502"
print(tes)
print(tes.encode().hex())

cut_data = []
dummy = ["O|1|2312019||^^^36\^^^37\^^^38\^^^39\^^^40\^^^41\^^^42\^^^43\^^^44\^^^45\^^^46\^^^47\^^^48\^^^49\^^^50\^^^51\^^^52\^^^53\^^^54\^^^55\^^^56\^^^57\^^^58\^^^59\^^^60\^^^61\^^^62\^^^63\^^^64\^^^65\^^^66\^^^67\^^^68\^^^69\^^^70\^^^71\^^^72\^^^73\^^^74|R|19900522105500|||||N||||1"]
max_chunk_data = 240  # doubled because using hex
for index, data in enumerate(dummy):
    if len(data) > max_chunk_data:
        chunks = [data[i:i + max_chunk_data] for i in range(0, len(data), max_chunk_data)]
        print(f"Print chunks: {chunks}")
        dummy.pop(index)
        cut_data.append(index)
        for i, chunk in enumerate(chunks):
            dummy.insert(i, chunk)

ENQ = b'\x05'  # ENQUIRY
ACK = b'\x06'  # ACKNOWLEDGE
NAK = b'\x15'  # NOT ACKNOWLEDGE
STX = b'\x02'  # START OF TEXT
ETX = b'\x03'  # END OF TEXT
ETB = b'\x17'  # PERTENGAHAN DATA
CR = b'\x0D'  #
LF = b'\x0A'  # LINE FEED
EOT = b'\x04'  # END OF DATA

for index, data in enumerate(dummy):
    # TAMBAHKAN INDEX DI AWAL DATA
    data = str(index + 1) + data

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
    checksum = calculate_checksum(data_for_checksum)
    print(f"Checksum Desimal: {checksum}")
    print(f"Checksum Hexadecimal: 0x{checksum:02x}")

curr_status= b'17'
ETB= b'\x17'
print(curr_status.decode('utf-8') == ETB.hex())
print(f'ETB: {type(ETB.hex())}')