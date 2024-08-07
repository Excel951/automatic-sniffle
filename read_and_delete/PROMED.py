import json
import time
import re
from dotenv import load_dotenv
from datetime import datetime
from utils import retrieve_data as rd
from utils import convert as conv
import os

load_dotenv()

class PROMED:
    def listing_file(self, path_folder):
        list_file = [file for file in os.listdir(path_folder)]
        return list_file

    def processing_data(self, file, path_folder_to_read):
        print(f'File name: {file}')
        path_read_file = os.path.join(path_folder_to_read, file)
        file = rd.retrieve_data_read_only(path_read_file)
        converted_data = conv.convert_hexa_to_ascii(file)
        data = self.ini_main(converted_data)
        datas = []
        for data in data:
            datas.append(data)
        return datas, path_read_file

    def write_file(self, path_folder_to_write, data):
        name = data[0][0]
        format_file = os.getenv('format_file')

        current_date = datetime.now()
        year, month, day, hour, minute, second = current_date.year, current_date.month, current_date.day, current_date.hour, current_date.minute, current_date.second
        name_file = f'{year}{str(month).zfill(2)}{str(day).zfill(2)}{str(hour).zfill(2)}{str(minute).zfill(2)}{str(second).zfill(2)}_PROMED_{data[0][0]}.{format_file}'
        path_write_file = os.path.join(path_folder_to_write, name_file)

        parsed_date = datetime.strptime(data[2][0], "%Y%m%d%H%M%S")
        formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

        dict = {'id': name, 'merk': 'AC 610', 'date': formatted_date, 'parameter': []}
        for i in range(len(data[1])):
            dict['parameter'].append(
                {
                    'parameter': data[1][i][0],
                    'nilai': data[1][i][1],
                    'success': 'true' if data[1][i][2] == '' else 'false',
                    'note': data[1][i][2],
                    'image': '-'
                }
            )

        with open(path_write_file, 'w') as file:
            file.write(json.dumps(dict))

        self.write_log(data[3], dict)

    def write_log(self, teks: str, string_json: dict):
        try:
            path_logs = os.getenv('path_logs')
            path_type_logs = os.getenv('path_logs_promed')
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

    def cleansing_and_retrieve_data_promed(self, result):
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

    def print_result(self, name, matches, date):
        try:
            parsed_date = datetime.strptime(date[0], "%Y%m%d%H%M%S")
            formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

            alat_string = 'ALAT: AC 610'
            waktu_string = f'WAKTU: {formatted_date}'
            id_string = f'NAMA PASIEN: {name[0]}'
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

        except Exception as e:
            print('Error di print_result')
            print(e)

    def add_note(self, matches):
        try:
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
        except Exception as e:
            print('Error di add_note')
            print(e)

    def ini_main(self, converted_data):
        try:
            name, matches, date = self.cleansing_and_retrieve_data_promed(result=converted_data)
            if name and matches and date:
                matches = self.add_note(matches)
                teks = self.print_result(name, matches, date)
                return [name, matches, date, teks]
            else:
                print("Bukan PROMED")
        except Exception as e:
            print("Bukan PROMED")

if __name__ == '__main__':
    try:
        list_file = []
        path_folder_to_read = 'transit_folder'
        path_folder_to_write = 'saved_data'
        while True:
            list_file = PROMED.listing_file(path_folder=path_folder_to_read)
            for file in list_file:
                if 'promed' in file.lower():
                    data, path_read_file = PROMED.processing_data(file, path_folder_to_read)
                    print(data)
                    PROMED.write_file(path_folder_to_write, data)
                    # os.remove(path_read_file)
            time.sleep(2)
            print('Kode berjalan')

    except Exception as e:
        print(e)