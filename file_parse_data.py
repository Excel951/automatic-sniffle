import re
import os

# RETRIEVE FILE HEX
name_file = "HEXA_XN1000_20240514_11-55.log.txt"
with open(os.path.join("./files_hexa", name_file), "r") as file:
    hexa_content = file.read()

# def convert_hexa_to_ascii(hexa_content):
# HAPUS CHAR YANG TIDAK DIPERLUKAN
pattern_hexa = r'0x([\w+\d+]{2})'

# BERSIHKAN HEXA DARI 0x YANG TIDAK DIPERLUKAN
hexa_cleaned = re.findall(pattern=pattern_hexa, string=hexa_content)

# GABUNGKAN HEX YANG TELAH BERSIH DALAM SATU VARIABEL
hexa_string = " ".join(hexa_cleaned)

# CONVERT DATA DARI HEX
result = bytearray.fromhex(hexa_string)
result = str(result)

# PATTERN DATA ASCII
# DATA
pattern_parameter_in_promed = r'[A-Z]\|\d+\|[A-Z]+\|[0-9-]+\^([A-Za-z\(\)%#*\-]+)\^\w+\|\|([0-9.]+)'
# NAMA
pattern_name_in_promed = r'PID\|\d+\|\|[^\|]*\|[^\|]*\|\^([A-Za-z\ \']+)'

# AMBIL DATA YANG DIPERLUKAN
# NAMA
name = re.findall(pattern=pattern_name_in_promed, string=result)
# DATA
matches = re.findall(pattern=pattern_parameter_in_promed, string=result)

# HAPUS UMUR
matches.pop(0)

print(f'Name: {name[0]}')
for match in matches:
    parameter, value = match
    print(f'Parameter: {parameter}, Nilai: {value}')