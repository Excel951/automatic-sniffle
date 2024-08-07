import json
import time
import re
from dotenv import load_dotenv
from datetime import datetime
from utils import retrieve_data as rd
from utils import convert as conv
import os

load_dotenv()

class AGD:
    def cleansing_and_retrieve_data_in_agd(self, data_in_ascii):
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
            data_hemoglobin_oxygen = [re.findall(pattern=pattern_data, string=string)[0] for string in
                                      dirty_data_hemoglobin_oxygen_result]

            return (
                date_result,
                patient_result,
                data_acid,
                data_hemoglobin_oxygen
            )
        except Exception as e:
            print('Error di cleansing_and_retrieve_data_in_agd')
            print(e)

    def print_result(self, date, id, matches):
        try:
            parsed_date = datetime.strptime(date[0], '%d-%b-%y %H:%M')
            formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M')

            alat_string = 'ALAT: AGD'
            waktu_string = f'WAKTU: {formatted_date}'
            id_string = f'PATIENT ID: {id[0]}'
            batas_acid = f'\nACID/BASE\nPARAMETER\t\tHASIL'
            batas_hemo = f'\nHEMOGLOBIN/OXYGEN STATUS\nPARAMETER\t\tHASIL'

            all_text = f'{alat_string}\n{waktu_string}\n{id_string}\n{batas_acid}\n'

            print(alat_string)
            print(waktu_string)
            print(id_string)
            # DATA ACID
            print(batas_acid)
            for match in matches[0]:
                parameter, value, note = match
                teks = f'{parameter}\t\t\t{value}\t\tNote: {note}'
                print(teks)
                all_text += f'{teks}\n'

            # DATA HEMO
            all_text += f'{batas_hemo}\n'
            print(batas_hemo)
            for match in matches[1]:
                parameter, value, note = match
                teks = f'{parameter}\t\t\t{value}\t\tNote: {note}'
                print(teks)
                all_text += f'{teks}\n'

            return all_text

        except Exception as e:
            print('Error di print_result')
            print(e)

    def add_note(self, matches):
        try:
            datas = []
            updated_matches = []
            for i in range(len(matches)):
                for match in matches[i]:
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
                datas.append(updated_matches)
                updated_matches = []
            return datas
        except Exception as e:
            print('Error di add_note')
            print(e)

    def ini_main(self, converted_data):
        try:
            date, identity, data_acid, data_hemoglobin_oxygen = self.cleansing_and_retrieve_data_in_agd(
                data_in_ascii=converted_data)
            if identity and data_acid and data_hemoglobin_oxygen and date:
                matches = self.add_note([data_acid, data_hemoglobin_oxygen])
                teks = self.print_result(date, identity, matches=matches)
                return [date, identity, matches, teks]
            else:
                print("Bukan AGD")
        except Exception as e:
            print("Bukan AGD")
    def listing_file(self, path_folder):
        list_file = [file for file in os.listdir(path_folder)]
        return list_file

    def processing_data(self, file, path_folder_to_read):
        print(f'File name: {file}')
        path_read_file = os.path.join(path_folder_to_read, file)
        file = rd.retrieve_data_read_only(path_read_file)
        converted_data = conv.convert_hexa_to_ascii(file)
        datas = self.ini_main(converted_data)
        updated_datas = []
        for data in datas:
            updated_datas.append(data)
        return updated_datas, path_read_file

    def write_file(self, path_folder_to_write, data):
        try:
            id = data[1][0]
            date = data[0][0]
            format_file = os.getenv('format_file')

            current_date = datetime.now()
            year, month, day, hour, minute, second = current_date.year, current_date.month, current_date.day, current_date.hour, current_date.minute, current_date.second
            name_file = f'{year}{month}{day}{hour}{minute}{second}_AGD_{id}.{format_file}'
            path_write_file = os.path.join(path_folder_to_write, name_file)

            parsed_date = datetime.strptime(date, '%d-%b-%y %H:%M')
            formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M')

            dict = {'id': id, 'merk': 'XN-10', 'date': formatted_date, 'parameter': []}
            for i in range(len(data[2][0])):
                dict['parameter'].append({'parameter': data[2][0][i][0], 'nilai': data[2][0][i][1], "success": 'true' if data[2][0][i][2] == '' else 'false', "note": data[2][0][i][2], 'image': '-'})
            for i in range(len(data[2][1])):
                dict['parameter'].append({'parameter': data[2][1][i][0], 'nilai': data[2][1][i][1], "success": 'true' if data[2][1][i][2] == '' else 'false', 'note': data[2][1][i][2], 'image': '-'})
            with open(path_write_file, 'w') as file:
                file.write(json.dumps(dict))

            self.write_log(data[3], dict)

        except Exception as e:
            print('Error di write_file')
            print(e)

    def write_log(self, teks: str, string_json: dict):
        try:
            path_logs = os.getenv('path_logs')
            path_type_logs = os.getenv('path_logs_agd')
            format_file = os.getenv('format_log')

            path = os.path.join(path_logs, path_type_logs)

            if not os.path.exists(path):
                os.makedirs(path)

            current_date = datetime.now()

            year, month, day, hour, minute, second = current_date.year, current_date.month, current_date.day, current_date.hour, current_date.minute, current_date.second
            name_file = f'{year}{str(month).zfill(2)}{str(day).zfill(2)}{str(hour).zfill(2)}{str(minute).zfill(2)}{str(second).zfill(2)}_{path_type_logs.upper()}.{format_file}'
            path_write_file = os.path.join(path, name_file)

            with open(path_write_file, 'w') as file:
                file.write(teks)
                file.write(json.dumps(string_json))

        except Exception as e:
            print('Error di write log')
            print(e)

if __name__ == '__main__':
    try:
        list_file = []
        path_folder_to_read = 'transit_folder'
        path_folder_to_write = 'saved_data'
        while True:
            list_file = AGD.listing_file(path_folder=path_folder_to_read)
            for file in list_file:
                if 'AGD' in file:
                    data, path_read_file = AGD.processing_data(file, path_folder_to_read)
                    print(data)
                    AGD.write_file(path_folder_to_write, data)
                    # os.remove(path_read_file)
            time.sleep(2)
            print('Kode berjalan')

    except Exception as e:
        print(e)