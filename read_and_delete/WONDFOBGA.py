import json
import time
import re
from dotenv import load_dotenv
from datetime import datetime
from parse_data.utils import retrieve_data as rd
from parse_data.utils import convert as conv
from parse_data import wondfobga
import os

load_dotenv()

class WONDFOBGA:
    def cleansing_and_retrieve_data_wondfobga(self, result):
        # PATTERN DATA ASCII
        # DATA                              OBX|NUM | NM |NUM | FIELD PARAMETER              | NUM ^^ |
        pattern_parameter_in_wondfobga = r"OBX\|\d+\|NM\|\d+\|([A-Za-z0-9\/\(\)\-\+\.]+)\|([\d+\.\-]+)"
        # NAMA
        pattern_name_in_wondfobga = r"PID\|\d+\|(\d+)\|\d+\^+\|\|(\w+\^*)"
        # DATE
        pattern_date = r'BGA-101.*\|(\d+).*\|ORU.*'

        # AMBIL DATA YANG DIPERLUKAN
        # DATA
        matches = re.findall(pattern=pattern_parameter_in_wondfobga, string=result)
        # NAMA
        name = re.findall(pattern=pattern_name_in_wondfobga, string=result)
        # DATE
        date = re.findall(pattern=pattern_date, string=result)

        id = name[0][0]
        name = name[0][1]

        # REPLACE ^ WITH SPACES
        if "^" in name:
            name = name.replace("^", " ")

        return id, name, matches, date[0]

    def print_result(self, id, name, matches, date):
        parsed_date = datetime.strptime(date, "%Y%m%d%H%M%S")
        formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

        alat_string = "ALAT: BGA-101"
        waktu_string = f'WAKTU: {formatted_date}'
        id_string = f'ID: {id}\nNAMA: {name}'
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

    def ini_main(self, converted_data):
        try:
            id, name, matches, date = self.cleansing_and_retrieve_data_wondfobga(converted_data)
            if id and name and matches and date:
                matches = self.add_note(matches)
                teks = self.print_result(id, name, matches, date)
                return [id, name, matches, date, teks]
            else:
                print("Bukan wondfobga")
        except Exception as e:
            print("Bukan wondfobga")

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
        format_file = os.getenv('format_file')
        current_date = datetime.now()

        year, month, day, hour, minute, second = current_date.year, current_date.month, current_date.day, current_date.hour, current_date.minute, current_date.second
        name_file = f'{year}{str(month).zfill(2)}{str(day).zfill(2)}{str(hour).zfill(2)}{str(minute).zfill(2)}{str(second).zfill(2)}_WONDFOBGA_{data[0]}_{data[1]}.{format_file}'
        path_write_file = os.path.join(path_folder_to_write, name_file)

        parsed_date = datetime.strptime(data[3], "%Y%m%d%H%M%S")
        formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

        dict = {'id': data[0], 'merk': 'BGA-101', 'date': formatted_date, 'parameter': []}
        for i in range(len(data[2])):
            dict['parameter'].append(
                {
                    'parameter': data[2][i][0],
                    'nilai': data[2][i][1],
                    'success': 'true' if data[2][i][2] == '' else 'false',
                    'note': data[2][i][2],
                    'image': '-'
                }
            )

        with open(path_write_file, 'w') as file:
            file.write(json.dumps(dict))

        self.write_log(data[4], dict)

    def write_log(self, teks: str, string_json: dict):
        try:
            path_logs = os.getenv('path_logs')
            path_type_logs = os.getenv('path_logs_wondfobga')
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
        path_folder_to_read = os.getenv('path_folder_to_read')
        path_folder_to_write = os.getenv('path_folder_to_write')
        while True:
            list_file = WONDFOBGA.listing_file(path_folder=path_folder_to_read)
            for file in list_file:
                if 'wondfobga' in file.lower():
                    data, path_read_file = WONDFOBGA.processing_data(file, path_folder_to_read)
                    print(data)
                    WONDFOBGA.write_file(path_folder_to_write, data)
                    # os.remove(path_read_file)
            time.sleep(2)
            print('Kode berjalan')

    except Exception as e:
        print(e)