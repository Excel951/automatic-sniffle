import re

def convert_hexa_to_ascii(hexa_content):
    if type(hexa_content) == bytes:
        hexa_content = hexa_content.decode("utf-8")

    # HAPUS CHAR YANG TIDAK DIPERLUKAN
    pattern_hexa = r'0x([\w+\d+]{2})'

    # BERSIHKAN HEXA DARI 0x YANG TIDAK DIPERLUKAN
    hexa_cleaned = re.findall(pattern=pattern_hexa, string=hexa_content)

    # GABUNGKAN HEX YANG TELAH BERSIH DALAM SATU VARIABEL
    hexa_string = " ".join(hexa_cleaned)

    # CONVERT DATA DARI HEX
    result = bytearray.fromhex(hexa_string)
    # result = str(result)
    result = result.decode("utf-8")

    return result