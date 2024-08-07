import re
import os
from datetime import datetime

from .utils import convert as hexa_to_ascii
from .utils import retrieve_data as rd
# from utils import convert as hexa_to_ascii
# from utils import retrieve_data as rd

# FINISHED

def cleansing_and_retrieve_data_wondfobga(result):
    # PATTERN DATA ASCII
    # DATA                              OBX|NUM | NM |NUM | FIELD PARAMETER              | NUM ^^ |
    pattern_parameter_in_wondfobga = r"OBX\|\d+\|NM\|\d+\|([A-Za-z0-9\/\(\)\-\+\.]+)\|([\d+\.\-]+)"
    # NAMA
    pattern_name_in_wondfobga = r"PID\|\d+\|(\d+)\|\d+\^+\|\|(\w+\^*)"
    # DATE
    pattern_date = r'BGA-101.*\|(\d+).*\|ORU.*'

    # AMBIL DATA YANG DIPERLUKAN
    # DATA
    matches = re.findall(pattern=pattern_parameter_in_wondfobga, string=result)
    # NAMA
    name = re.findall(pattern=pattern_name_in_wondfobga, string=result)
    # DATE
    date = re.findall(pattern=pattern_date, string=result)

    id = name[0][0]
    name = name[0][1]

    # REPLACE ^ WITH SPACES
    if "^" in name:
        name = name.replace("^", " ")

    return id, name, matches, date[0]

def print_result(id, name, matches, date):
    parsed_date = datetime.strptime(date, "%Y%m%d%H%M%S")
    formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    print("ALAT: BGA-101")
    print(f'WAKTU: {formatted_date}')
    print(f'ID: {id}\nNAMA: {name}')
    print("PARAMETER\t\tHASIL")
    for match in matches:
        parameter, value, note = match
        print(f'{parameter}\t\t\t{value}\t\tNote: {note}')

def add_note(matches):
    updated_matches = []
    for match in matches:
        parameter, value = match
        if value is None:
            note = 'undefined'
        elif re.search(r'\s+', value):
            note = 'nilai parameter kosong'
        elif value == '0.0':
            note = 'nilai parameter 0.0'
        else:
            note = ''  # No additional note in this case
        updated_match = (parameter, value, note)
        updated_matches.append(updated_match)
    return updated_matches

def ini_main(converted_data):
    try:
        id, name, matches, date = cleansing_and_retrieve_data_wondfobga(converted_data)
        if id and name and matches and date:
            matches = add_note(matches)
            print_result(id, name, matches, date)
            return (id, name, matches, date)
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
    id, name, matches, date = cleansing_and_retrieve_data_wondfobga(result=result)
    matches = add_note(matches)
    print_result(id, name, matches, date)