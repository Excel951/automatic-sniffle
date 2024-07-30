import re
import os
from .utils import retrieve_data as rd
from .utils import convert as hexa_to_ascii

# FINISHED

def cleansing_and_retrieve_data_exias(result):
    # PATTERN DATA ASCII
    # DATA
    pattern_parameter_in_exias = r'[A-Z]\|\d+\|\^{3}(\w+)\^+\w+\|(\d+(?:\.\d+)?)\|'

    # AMBIL DATA YANG DIPERLUKAN
    # DATA
    matches = re.findall(pattern=pattern_parameter_in_exias, string=result)

    return matches

def print_result(matches):
    print("Result EXIAS")
    for match in matches:
        parameter, value = match
        print(f'Parameter: {parameter}, Nilai: {value}')

def ini_main(converted_data):
    try:
        matches = cleansing_and_retrieve_data_exias(result=converted_data)
        print(f'Exias: {matches}')
        if matches:
            print_result(matches)
            return matches
        else:
            print("Bukan EXIAS")
    except Exception as e:
        print("Bukan EXIAS")
    # return matches

if __name__ == '__main__':
    name_file = "HEXA_EXIAS_20240613_01-19.log.txt"
    parent_file_path = os.path.join("../files_hexa", name_file)

    hexa_content = rd.retrieve_data_read_only(path_file=parent_file_path)
    result = hexa_to_ascii.convert_hexa_to_ascii(hexa_content=hexa_content)
    matches = cleansing_and_retrieve_data_exias(result=result)
    print_result(matches)