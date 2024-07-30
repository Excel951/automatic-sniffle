import re
import os
from .utils import convert as hexa_to_ascii
from .utils import retrieve_data as rd

# FINISHED

def cleansing_and_retrieve_data_promed(result):
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

    return name, matches

def print_result(name, matches):
    print('Promed')
    print(f'Name: {name[0]}')
    for match in matches:
        parameter, value = match
        print(f'Parameter: {parameter}, Nilai: {value}')

def ini_main(converted_data):
    try:
        name, matches = cleansing_and_retrieve_data_promed(result=converted_data)
        if name and matches:
            print_result(name, matches)
            return (name, matches)
        else:
            print("Bukan PROMED")
    except Exception as e:
        print("Bukan PROMED")

if __name__ == '__main__':
    name_file = "HEXA_PROMED_20240613_02-36.log.txt"
    hexa_content = rd.retrieve_data_read_only(path_file=os.path.join('../files_hexa', name_file))

    result = hexa_to_ascii.convert_hexa_to_ascii(hexa_content=hexa_content)
    name, matches = cleansing_and_retrieve_data_promed(result=result)
    print_result(name, matches)