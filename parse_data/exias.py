import re
import os
from datetime import datetime

from .utils import retrieve_data as rd
from .utils import convert as hexa_to_ascii
# from utils import retrieve_data as rd
# from utils import convert as hexa_to_ascii


# FINISHED

def cleansing_and_retrieve_data_exias(result):
    # PATTERN DATA ASCII
    # DATA
    # pattern_parameter_in_exias = r'[A-Z]\|\d+\|\^{3}(\w+)\^+\w+\|(\d+(?:\.\d+)?)\|'
    pattern_parameter_in_exias = r'[A-Z]\|\d+\|\^{3}(\w+)\^+\w+\|(\d+(?:\.\d*)?|\s*)\|'
    pattern_merk = r'H.+\|{3}([\w\d\-]*)\^\w+\^'
    pattern_date = r'H\|.+\|\|(\d{14})'
    pattern_id = r'P\|1\|{2}([\w\d]+)\|'

    # AMBIL DATA YANG DIPERLUKAN
    # DATA
    matches = re.findall(pattern=pattern_parameter_in_exias, string=result)
    merk = re.findall(pattern=pattern_merk, string=result)
    date = re.findall(pattern=pattern_date, string=result)
    id = re.findall(pattern=pattern_id, string=result)

    return matches, merk[0], date[0], id[0]


def print_result(matches, merk, date, id):
    parsed_date = datetime.strptime(date, "%Y%m%d%H%M%S")
    formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    print(f"ALAT: {merk}")
    print(f"WAKTU: {formatted_date}")
    print(f'ID: {id}')
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
        elif value == '':
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
        matches, merk, date, id = cleansing_and_retrieve_data_exias(result=converted_data)
        if matches:
            matches = add_note(matches)
            print_result(matches, merk, date, id)
            return [matches, merk, date, id]
        else:
            print("Bukan EXIAS")
    except Exception as e:
        print("Bukan EXIAS")
    # return matches


if __name__ == '__main__':
    name_file = "../files_hexa/HEXA_EXIAS_20240725_08-31.log.txt"
    parent_file_path = os.path.join("../files_hexa", name_file)

    hexa_content = rd.retrieve_data_read_only(path_file=parent_file_path)
    result = hexa_to_ascii.convert_hexa_to_ascii(hexa_content=hexa_content)
    matches, merk, date, id = cleansing_and_retrieve_data_exias(result=result)
    matches = add_note(matches)
    print_result(matches, merk, date, id)
