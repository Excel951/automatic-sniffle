import re
import os
from .utils import retrieve_data as rd
from .utils import convert

# NOT FINISHED

def cleansing_and_retrieve_data_in_agd(result):

    # AMBIL DATA BERDASARKAN KATEGORI
    # PATTERN DATA ASCII
    patient_pattern = r'^ID:\s*([\d]*)\b'
    parameter_pattern = r'([*A-Z]{2,3}|pH|SG)\s+([\d+-.]*)\s*[a-zA-Z/]*?'
    # parameter_pattern = r'([*A-Za-z]+)\s+([\d+-.]*)\s+\w*\d*\/*'

    # IMPLEMENTASI PATTERN DI ATAS
    patient_result = re.findall(pattern=patient_pattern, string=result)
    data_result = re.findall(pattern=parameter_pattern, string=result)

    return (
        patient_result,
        data_result
    )

def print_result(id, matches):
    print('U500Insight')
    if id:
        print(f'Patient ID: {id[0]}')
    else:
        print(f'Patient ID: 00000')
    for match in matches:
        parameter, value = match
        print(f'{parameter}:\t\t{value}')

def ini_main(converted_data):
    try:
        identity, data_result = cleansing_and_retrieve_data_in_agd(result=converted_data)
        if identity or data_result:
            print_result(identity, data_result)
            return (identity, data_result)
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

    identity, data_result = cleansing_and_retrieve_data_in_agd(result=result)

    print_result(identity, matches=data_result)