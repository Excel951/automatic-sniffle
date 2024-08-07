from datetime import datetime
import re, os
from .utils import retrieve_data as rd
from .utils import convert
# from utils import retrieve_data as rd
# from utils import convert

# import sys
# import os
#
# # Tambahkan path dari direktori parent ke sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# FINISHED

def cleansing_and_retrieve_data_in_agd(data_in_ascii):
    try:
        # CLEAN ALL NON PRINTABLE
        file_ascii = data_in_ascii.replace('', '')

        # AMBIL DATA BERDASARKAN KATEGORI
        # PATTERN DATA ASCII
        date_pattern = r'.*Patient Report\s*([\w\d\-\:\ ]*)\s*PATIENT.*'
        patient_pattern = r'Patient ID:\|*\s*(\d+)'
        acid_base_pattern = r'(pH\s+\d+\.\d+[\s\S]+?stHCO3\s+\d+\.\d+\s+mmol/L)'
        hemoglobin_oxygen_pattern = r'(tHb\s+\d+\.\d+\s+g/dL[\s\S]+?O2Ct\s+\d+\.\d+\s+%vol)'

        # IMPLEMENTASI PATTERN DI ATAS
        date_result = re.findall(pattern=date_pattern, string=file_ascii)
        patient_result = re.findall(pattern=patient_pattern, string=file_ascii)
        dirty_data_acid_base_result = re.findall(pattern=acid_base_pattern, string=file_ascii)
        dirty_data_hemoglobin_oxygen_result = re.findall(pattern=hemoglobin_oxygen_pattern, string=file_ascii)

        # BERSIHKAN KODE \n DAN \r
        dirty_data_acid_base_result = dirty_data_acid_base_result[0].split('\r\n')
        dirty_data_hemoglobin_oxygen_result = dirty_data_hemoglobin_oxygen_result[0].split('\r\n')

        # AMBIL DATA DAN PARAMETER
        pattern_data = r'([\w\d()]+)\s+([\d+.-]+)'
        data_acid = [re.findall(pattern=pattern_data, string=string)[0] for string in dirty_data_acid_base_result]
        data_hemoglobin_oxygen = [re.findall(pattern=pattern_data, string=string)[0] for string in dirty_data_hemoglobin_oxygen_result]

        return (
            date_result,
            patient_result,
            data_acid,
            data_hemoglobin_oxygen
        )
    except Exception as e:
        print('Error di cleansing_and_retrieve_data_in_agd')
        print(e)

def print_result(date, id, matches):
    try:
        parsed_date = datetime.strptime(date[0], '%d-%b-%y %H:%M')
        formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M')
        print('ALAT: AGD')
        print(f'WAKTU: {formatted_date}')
        print(f'PATIENT ID: {id[0]}')
        # DATA ACID
        print(f'\nACID/BASE')
        print(f'PARAMETER\t\tHASIL')
        for match in matches[0]:
            param, value, note = match
            print(f'{param}\t\t{value}\t\t\tNote: {note}')

        print(f'\nHEMOGLOBIN/OXYGEN STATUS')
        print(f'PARAMETER\t\tHASIL')
        for match in matches[1]:
            parameter, value, note = match
            print(f'{parameter}\t\t{value}\t\t\tNote: {note}')
    except Exception as e:
        print('Error di print_result')
        print(e)

def add_note(matches):
    try:
        datas = []
        updated_matches = []
        for i in range(len(matches)):
            for match in matches[i]:
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
            datas.append(updated_matches)
            updated_matches = []
        return datas
    except Exception as e:
        print('Error di add_note')
        print(e)

def ini_main(converted_data):
    try:
        date, identity, data_acid, data_hemoglobin_oxygen = cleansing_and_retrieve_data_in_agd(data_in_ascii=converted_data)
        if identity and data_acid and data_hemoglobin_oxygen and date:
            matches = add_note([data_acid, data_hemoglobin_oxygen])
            print_result(date, identity, matches=matches)
            return (date, identity, matches)
        else:
            print("Bukan AGD")
    except Exception as e:
        print("Bukan AGD")

if __name__ == '__main__':
    name_file = "HEXA_AGD_20240129_04-57.log.txt"
    parent_file_path = os.path.join("../files_hexa/", name_file)
    hexa_content = rd.retrieve_data_read_only(path_file=parent_file_path)
    result = convert.convert_hexa_to_ascii(hexa_content=hexa_content)

    date, identity, data_acid, data_hemoglobin_oxygen = cleansing_and_retrieve_data_in_agd(data_in_ascii=result)
    matches = add_note([data_acid, data_hemoglobin_oxygen])
    print(f'Matches: {matches}')
    print_result(date, identity, matches=matches)