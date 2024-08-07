import re
import os
from .utils import retrieve_data as rd
from .utils import convert
# from utils import retrieve_data as rd
# from utils import convert

# FINISHED

def cleansing_and_retrieve_data_in_agd(result):

    # AMBIL DATA BERDASARKAN KATEGORI
    # PATTERN DATA ASCII
    patient_pattern = r'^ID:\s*([\d]*)\b'
    parameter_pattern = r'([*A-Z]{2,3}|pH|SG)\s+([\d+-.]*)\s*[a-zA-Z/]*?'
    # parameter_pattern = r'([*A-Za-z]+)\s+([\d+-.]*)\s+\w*\d*\/*'
    date_pattern = r'.*\s+([\d\-\:\s]*)\s+ID'

    # IMPLEMENTASI PATTERN DI ATAS
    patient_result = re.findall(pattern=patient_pattern, string=result)
    data_result = re.findall(pattern=parameter_pattern, string=result)
    date_result = re.findall(date_pattern, string=result)

    return (
        patient_result,
        data_result,
        date_result[0].strip()
    )

def print_result(id, matches, date):
    print('ALAT: U500Insight')
    print(f'WAKTU: {date}')
    if id:
        print(f'ID: {id[0]}')
    else:
        print(f'ID: 00000')
    print("PARAMETER\t\tHASIL")
    for match in matches:
        parameter, value, note = match
        print(f'{parameter}\t\t{value}\t\t\tNote: {note}')

def add_note(matches):
    updated_matches = []
    for match in matches:
        parameter, value = match
        if value is None:
            note = 'undefined'
        elif value == '':
            note = 'nilai parameter kosong'
        elif value == '0.0':
            note = 'nilai parameter 0.0'
        elif value == '-':
            note = 'nilai negatif'
        elif value == '+':
            note = 'nilai positif'
        elif value == '+-':
            note = 'trace'
        else:
            note = ''  # No additional note in this case
        updated_match = (parameter, value, note)
        updated_matches.append(updated_match)
    return updated_matches

def ini_main(converted_data):
    try:
        identity, data_result, date = cleansing_and_retrieve_data_in_agd(result=converted_data)
        if identity or data_result and date:
            data_result = add_note(data_result)
            print_result(identity, data_result, date)
            return (identity, data_result, date)
        else:
            print("Bukan U500Insight")
    except Exception as e:
        print("Bukan U500Insight")

if __name__ == '__main__':
    name_file = "HEXAU500Insight20240129_05-55.log.txt"
    parent_file_path = os.path.join("../files_hexa/", name_file)
    hexa_content = rd.retrieve_data_read_only(path_file=parent_file_path)

    result = convert.convert_hexa_to_ascii(hexa_content=hexa_content)
    # print(result)

    identity, data_result, date = cleansing_and_retrieve_data_in_agd(result=result)
    data_result = add_note(data_result)

    print_result(identity, data_result, date)