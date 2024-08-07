import os
import re
import json
import time
from datetime import datetime
from utils import retrieve_data as rd
from utils import convert as conv
from dotenv import load_dotenv

load_dotenv()

class Exias:
    def cleansing_and_retrieve_data_exias(self, result):
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

    def print_result(self, matches, merk, date, id):
        parsed_date = datetime.strptime(date, "%Y%m%d%H%M%S")
        formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

        alat_string = f"ALAT: {merk}"
        waktu_string = f"WAKTU: {formatted_date}"
        id_string = f'ID: {id}'
        batas = "PARAMETER\t\tHASIL"

        all_text = f'{alat_string}\n{waktu_string}\n{id_string}\n{batas}\n'

        print(alat_string)
        print(waktu_string)
        print(id_string)
        print(batas)
        for match in matches:
            parameter, value, note = match
            teks = f'{parameter}\t\t\t{value}\t\tNote: {note}'
            print(teks)
            all_text += f'{teks}\n'
        return all_text

    def add_note(self, matches):
        updated_matches = []
        for match in matches:
            parameter, value = match
            if value is None:
                note = self, 'undefined'
            elif value == '':
                note = 'nilai parameter kosong'
            elif value == '0.0':
                note = 'nilai parameter 0.0'
            else:
                note = ''  # No additional note in this case
            updated_match = (parameter, value, note)
            updated_matches.append(updated_match)
        return updated_matches

    def lich_data(self, converted_data):
        try:
            matches, merk, date, id = self.cleansing_and_retrieve_data_exias(result=converted_data)
            if matches:
                matches = self.add_note(matches)
                teks = self.print_result(matches, merk, date, id)
                return [matches, merk, date, id, teks]
            else:
                print("Bukan EXIAS")
        except Exception as e:
            print("Bukan EXIAS")

    def listing_file(self, path_folder):
        list_file = [file for file in os.listdir(path_folder)]
        return list_file

    def processing_data(self, file, path_folder_to_read):
        print(f'File name: {file}')
        path_read_file = os.path.join(path_folder_to_read, file)
        file = rd.retrieve_data_read_only(path_read_file)
        converted_data = conv.convert_hexa_to_ascii(file)
        data = self.lich_data(converted_data)
        datas = []
        for data in data:
            datas.append(data)
        return datas, path_read_file

    def write_file(self, path_folder_to_write, data):
        format_file = os.getenv('format_file')

        current_date = datetime.now()
        year, month, day, hour, minute, second = current_date.year, current_date.month, current_date.day, current_date.hour, current_date.minute, current_date.second
        name_file = f'{year}{str(month).zfill(2)}{str(day).zfill(2)}{str(hour).zfill(2)}{str(minute).zfill(2)}{str(second).zfill(2)}_EXIAS_{data[3]}.{format_file}'
        path_write_file = os.path.join(path_folder_to_write, name_file)

        parsed_date = datetime.strptime(data[2], "%Y%m%d%H%M%S")
        formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

        dict = {'id': data[3], 'merk': f'{data[1]}', 'date': formatted_date, 'parameter': []}
        for i in range(len(data[0])):
            dict['parameter'].append(
                {
                    'parameter': data[0][i][0],
                    'nilai': data[0][i][1],
                    'success': 'true' if data[0][i][2] == '' else 'false',
                    'note': data[0][i][2],
                    'image': '-'
                }
            )

        with open(path_write_file, 'w') as file:
            file.write(json.dumps(dict))

        self.write_log(data[4], dict)

    def write_log(self, teks: str, string_json: dict):
        try:
            path_logs = os.getenv('path_logs')
            path_type_logs = os.getenv('path_logs_exias')
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
        exias = Exias()
        while True:
            list_file = exias.listing_file(path_folder=path_folder_to_read)
            for file in list_file:
                if 'exias' in file.lower():
                    data, path_read_file = exias.processing_data(file, path_folder_to_read)
                    print(data)
                    exias.write_file(path_folder_to_write, data)
                    # os.remove(path_read_file)
            time.sleep(2)
            print('Kode berjalan')

    except Exception as e:
        print(e)