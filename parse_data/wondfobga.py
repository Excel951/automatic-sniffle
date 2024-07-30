import re
import os
from .utils import convert as hexa_to_ascii
from .utils import retrieve_data as rd

# FINISHED

def cleansing_and_retrieve_data_wondfobga(result):
    # PATTERN DATA ASCII
    # DATA                              OBX|NUM | NM |NUM | FIELD PARAMETER              | NUM ^^ |
    pattern_parameter_in_wondfobga = r"OBX\|\d+\|NM\|\d+\|([A-Za-z0-9\/\(\)\-\+\.]+)\|([\d+\.\-]+)"
    # NAMA
    pattern_name_in_wondfobga = r"PID\|\d+\|(\d+)\|\d+\^+\|\|(\w+\^*)"

    # AMBIL DATA YANG DIPERLUKAN
    # DATA
    matches = re.findall(pattern=pattern_parameter_in_wondfobga, string=result)
    # NAMA
    name = re.findall(pattern=pattern_name_in_wondfobga, string=result)
    id = name[0][0]
    name = name[0][1]

    # REPLACE ^ WITH SPACES
    if "^" in name:
        name = name.replace("^", " ")

    return id, name, matches

def print_result(id, name, matches):
    print("Result WondFoBGA")
    print(f'ID: {id}\nName: {name}')
    for match in matches:
        parameter, value = match
        print(f'Parameter: {parameter}, Nilai: {value}')

def ini_main(converted_data):
    try:
        id, name, matches = cleansing_and_retrieve_data_wondfobga(converted_data)
        if id and name and matches:
            print_result(id, name, matches)
            return (id, name, matches)
        else:
            print("Bukan wondfobga")
    except Exception as e:
        print("Bukan wondfobga")

if __name__ == '__main__':
    # file_charc = 'CHARC_WondFoBGA_20240613_01-31.log.txt'
    file_hexa = 'HEXA_WondFoBGA_20240613_01-31.log.txt'
    parent_file_hexa = os.path.join('../files_hexa', file_hexa)

    # AMBIL DATA
    hexa_content = rd.retrieve_data_read_only(parent_file_hexa)

    # CONVERT HEXA TO ASCII
    result = hexa_to_ascii.convert_hexa_to_ascii(hexa_content=hexa_content)

    # RETRIEVE DATA FROM HL7
    id, name, matches = cleansing_and_retrieve_data_wondfobga(result=result)
    print_result(id, name, matches)