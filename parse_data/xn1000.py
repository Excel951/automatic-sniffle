import re
import os
from datetime import datetime
from .utils import convert
from .utils import retrieve_data as rd
# from utils import convert
# from utils import retrieve_data as rd

# FINISHED

def cleansing_and_retrieve_data_xn1000(result):
    try:
        # PATTERN DATA ASCII
        # DATA                          R/0/P/H|NUM |^^^param | FIELD PARAMETER              | NUM ^^ |
        # pattern_parameter_in_xn1000 = r"R\|\d+\|\^{4}([\w\%\#\-]+)\^*\d+\|([\d+\.\-]+).*([0-9]{14})"
        pattern_parameter_in_xn1000 = r"R\|\d+\|\^{4}([\w\%\#\-]+)\^*\d+\|([\d+\.\-]+)"
        pattern_id = r"O.*\^{2}(\d+)"
        pattern_date = r'R.*\|{4}(\d{14})'
        # AMBIL DATA YANG DIPERLUKAN
        # DATA
        matches = re.findall(pattern=pattern_parameter_in_xn1000, string=result)
        id = re.findall(pattern=pattern_id, string=result)
        date = re.findall(pattern=pattern_date, string=result)

        # print(f"Date: {date}")
        return matches, id[0], date

    except Exception as e:
        print('Error di regex')
        print(e)

def print_result(matches, id, date):
    try:

        print("ALAT: XN-10")
        parsed_date = datetime.strptime(date[0], "%Y%m%d%H%M%S")
        formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        print(f"WAKTU: {formatted_date}")
        print(f"PATIENT ID: {id}")
        print("PARAMETER\t\tHASIL")
        for match in matches:
            parameter, value, note = match
            print(f'{parameter}\t\t\t{value}\t\tNote: {note}')

    except Exception as e:
        print('Error di print result')
        print(e)

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
        matches, id, date = cleansing_and_retrieve_data_xn1000(converted_data)
        if matches:
            matches = add_note(matches)
            print_result(matches, id, date)
            return matches, id, date
        else:
            print("Bukan XN1000")
    except Exception as e:
        print("Bukan XN1000")

if __name__ == '__main__':
    name_file = "HEXA_XN1000_20240514_11-55.log.txt"
    # name_file = "CHARC_XN1000_20240514_11-55.log.txt"
    parent_file_path = os.path.join('../files_hexa', name_file)

    hexa_content = rd.retrieve_data_read_only(parent_file_path)
    result = convert.convert_hexa_to_ascii(hexa_content=hexa_content)
    matches, id, date = cleansing_and_retrieve_data_xn1000(result=result)
    matches = add_note(matches)
    print_result(matches, id, date)