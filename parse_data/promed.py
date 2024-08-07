import re
import os
from datetime import datetime

from .utils import convert as hexa_to_ascii
from .utils import retrieve_data as rd
# from utils import convert as hexa_to_ascii
# from utils import retrieve_data as rd

# FINISHED

def cleansing_and_retrieve_data_promed(result):
    try:
        # PATTERN DATA ASCII
        # DATA
        pattern_parameter_in_promed = r'[A-Z]\|\d+\|[A-Z]+\|[0-9-]+\^([A-Za-z\(\)%#*\-]+)\^\w+\|\|([0-9.]+)'
        # NAMA
        pattern_name_in_promed = r'PID\|\d+\|\|[^\|]*\|[^\|]*\|\^([A-Za-z\ \']+)'
        # DATE
        pattern_date_in_promed = r'.*Analyzer\|{3}(\d+).\d+.*'

        # AMBIL DATA YANG DIPERLUKAN
        # NAMA
        name = re.findall(pattern=pattern_name_in_promed, string=result)
        # DATA
        matches = re.findall(pattern=pattern_parameter_in_promed, string=result)
        # DATE
        date = re.findall(pattern=pattern_date_in_promed, string=result)

        # HAPUS UMUR
        matches.pop(0)

        return name, matches, date
    except Exception as e:
        print('Error di cleansing_and_retrieve_data_promed')
        print(e)

def print_result(name, matches, date):
    try:
        parsed_date = datetime.strptime(date[0], "%Y%m%d%H%M%S")
        formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

        print('ALAT: AC 610')
        print(f'WAKTU: {formatted_date}')
        print(f'NAMA PASIEN: {name[0]}')
        print("PARAMETER\t\tHASIL")
        for match in matches:
            parameter, value, note = match
            print(f'{parameter}\t\t\t{value}\t\tNote: {note}')

    except Exception as e:
        print('Error di print_result')
        print(e)

def add_note(matches):
    try:
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
    except Exception as e:
        print('Error di add_note')
        print(e)

def ini_main(converted_data):
    try:
        name, matches, date = cleansing_and_retrieve_data_promed(result=converted_data)
        if name and matches and date:
            matches = add_note(matches)
            print_result(name, matches, date)
            return (name, matches, date)
        else:
            print("Bukan PROMED")
    except Exception as e:
        print("Bukan PROMED")

if __name__ == '__main__':
    name_file = "HEXA_PROMED_20240613_02-36.log.txt"
    hexa_content = rd.retrieve_data_read_only(path_file=os.path.join('../files_hexa', name_file))

    result = hexa_to_ascii.convert_hexa_to_ascii(hexa_content=hexa_content)
    name, matches, date = cleansing_and_retrieve_data_promed(result=result)
    matches = add_note(matches)
    print_result(name, matches, date)