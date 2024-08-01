# import re
# # def calculate_checksum(frame):
# #     # Menghapus karakter start dan end (jika ada)
# #     frame_data = re.findall(r'<STX>(.*<CR><ETX>)[\d\w]+<CR><LF>', frame)
# #     tes = frame_data[0]
# #     checksum = sum(tes.encode('ascii')) % 256
# #     return checksum
# #
# # data = "<STX>2P|1||PID12345||LASTNAME^FIRSTNAME||19641223|M|||||Prescriptor||||||||||||Location<CR><ETX>D6<CR><LF>"
# # print(f"Checksum: {calculate_checksum(data)}")
# def calculate_checksum(data):
#     # Menghapus karakter kontrol seperti <STX>, <CR>, <ETX>, dan <LF>
#     # frame_data = re.findall(r'<STX>(.*<CR><ETX>)[\d\w]+<CR><LF>', data)
#     # print(frame_data[0])
#     # Menghitung checksum dengan menjumlahkan byte ASCII dan mengambil modulus 256
#     checksum = sum(data.encode('ascii')) % 256
#     return checksum
#
# # Data yang diberikan
# # data = "<STX>1H|\^&|||ABX|||||||P|E1394-97|20050111111502<CR><ETX>47<CR><LF>"
# data = "31487c5c5e267c7c7c4142587c7c7c7c7c7c7c507c45313339342d39377c32303035303131313131313530320D03"
#
# # Nilai checksum yang diberikan (dalam heksadesimal)
# given_checksum_hex = "59"
# given_checksum = int(given_checksum_hex, 16)
#
# # Hitung checksum dari data
# calculated_checksum = calculate_checksum(data)
# print(f"Calculated Checksum: {calculated_checksum}")
# print(f"Calculated Checksum: {hex(calculated_checksum)}")
#
# # Verifikasi checksum
# if calculated_checksum == given_checksum:
#     print("Checksum is correct.")
# else:
#     print("Checksum is incorrect.")

# a = "1H|\^&|||ABX|||||||P|E1394-97|20031118154840"
# STX = [0X02]
# print(f'{a.encode().hex()}')

# a = b'0231487c5e267c7c7c53656e6465725e49447c7c7c32303234303733313132303030307c7c7c7c7c507c317c32303234303733313132303030300d03fe0d0a0232507c317c3132333435367c7c446f655e4a6f686e7c7c31393630303130317c4d7c7c7c313233204d61696e2053745e5e416e79746f776e5e414e5e31323334357c3132332d3435362d373839307c7c7c7c7c7c7c7c7c0d03fb0d0a0233507c327c3738393130317c536d6974685e4a616e657c7c31393735303332337c467c7c7c343536204f616b2053745e5e4f74686572746f776e5e4f545e36373839307c3938372d3635342d333231307c7c7c7c7c7c7c7c7c0d0330d0a02344f7c317c4f52443132337c54657374436f6465315e546573744465736372697074696f6e315e5e5e7c7c7c32303234303733313132303030307c7c7c7c7c7c317c7c7c7c7c7c7c460d03a90d0a02354f7c327c4f52443132347c54657374436f6465325e546573744465736372697074696f6e325e5e5e7c7c7c32303234303733313132303030307c7c7c7c7c7c327c7c7c7c7c7c7c460d03af0d0a02364f7c337c4f52443132357c54657374436f6465335e546573744465736372697074696f6e335e5e5e7c7c7c32303234303733313132303030307c7c7c7c7c7c337c7c7c7c7c7c7c460d03b50d0a02374c7c317c4e0d03fa0d0a'
# STX = b'\x02'  # START OF TEXT
# stx=STX.hex()
# a_decode = a.decode()
# if STX.hex() in a.decode():
#     print(STX)