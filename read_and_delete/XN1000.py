import json
import time
import re
from dotenv import load_dotenv
from datetime import datetime
from utils import retrieve_data as rd
from utils import convert as conv
import os

load_dotenv()

class XN1000:
    def listing_file(self, path_folder):
        list_file = [file for file in os.listdir(path_folder)]
        return list_file

    def processing_data(self, file, path_folder_to_read):
        try:
            print(f'File name: {file}')
            path_read_file = os.path.join(path_folder_to_read, file)
            file = rd.retrieve_data_read_only(path_read_file)
            converted_data = conv.convert_hexa_to_ascii(file)
            data, id, date, teks = self.ini_main(converted_data)
            datas = []
            for data in data:
                datas.append([data[0], data[1], data[2]])
            return datas, id, path_read_file, date, teks

        except Exception as e:
            print('Error di processing data')
            print(e)


    def write_file(self, path_folder_to_write, data, id, date, teks):
        format_file = os.getenv('format_file')

        current_date = datetime.now()
        year, month, day, hour, minute, second = current_date.year, current_date.month, current_date.day, current_date.hour, current_date.minute, current_date.second
        name_file = f'{year}{str(month).zfill(2)}{str(day).zfill(2)}{str(hour).zfill(2)}{str(minute).zfill(2)}{str(second).zfill(2)}_XN1000_{id}.{format_file}'
        path_write_file = os.path.join(path_folder_to_write, name_file)

        parsed_date = datetime.strptime(date[0], "%Y%m%d%H%M%S")
        formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

        dict = {'id': id, 'merk': 'XN-10', 'date': formatted_date, 'parameter': []}
        for i in range(len(data)):
            dict['parameter'].append(
                {
                    'parameter': data[i][0],
                    'nilai': data[i][1],
                    'success': 'true' if data[i][2] == '' else 'false',
                    'note': data[i][2],
                    'image': '-'
                }
            )
        with open(path_write_file, 'w') as file:
            file.write(json.dumps(dict))

        self.write_log(teks, dict)

    def write_log(self, teks: str, string_json: dict):
        try:
            path_logs = os.getenv('path_logs')
            path_type_logs = os.getenv('path_logs_xn1000')
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

    def cleansing_and_retrieve_data_xn1000(self, result):
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

    def print_result(self, matches, id, date):
        try:
            parsed_date = datetime.strptime(date[0], "%Y%m%d%H%M%S")
            formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

            alat_string = "ALAT: XN-10"
            waktu_string = f"WAKTU: {formatted_date}"
            id_string = f"PATIENT ID: {id}"
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
            print('Error di print result')
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
            print('Error di add note')
            print(e)

    def ini_main(self, converted_data):
        try:
            matches, id, date = self.cleansing_and_retrieve_data_xn1000(converted_data)
            print(matches, id, date)
            if matches:
                noted_matches = self.add_note(matches)
                teks = self.print_result(noted_matches, id, date)
                return noted_matches, id, date, teks
            else:
                print("Bukan XN1000")
        except Exception as e:
            print("Bukan XN1000")
            print(e)

if __name__ == '__main__':
    try:
        list_file = []
        path_folder_to_read = 'transit_folder'
        path_folder_to_write = 'saved_data'
        while True:
            list_file = XN1000.listing_file(path_folder=path_folder_to_read)
            for file in list_file:
                if 'XN1000' in file:
                    data, path_read_file = XN1000.processing_data(file, path_folder_to_read)
                    print(data)
                    XN1000.write_file(path_folder_to_write, data)
                    # os.remove(path_read_file)
            time.sleep(2)
            print('Kode berjalan')

    except Exception as e:
        print(e)
