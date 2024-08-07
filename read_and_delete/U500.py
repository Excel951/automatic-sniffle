import json
import time
import re
from datetime import datetime
from dotenv import load_dotenv
from parse_data.utils import retrieve_data as rd
from parse_data.utils import convert as conv
from parse_data import U500Insight
import os

load_dotenv()

class U500:
    def listing_file(self, path_folder):
        list_file = [file for file in os.listdir(path_folder)]
        return list_file

    def processing_data(self, file, path_folder_to_read):
        try:
            print(f'File name: {file}')
            path_read_file = os.path.join(path_folder_to_read, file)
            file = rd.retrieve_data_read_only(path_read_file)
            converted_data = conv.convert_hexa_to_ascii(file)
            data = self.ini_main(converted_data)
            datas = []
            for data in data:
                datas.append(data)
            return datas, path_read_file
        except Exception as e:
            print('Error in processing data')
            print(e)

    def write_file(self, path_folder_to_write, data):
        try:
            format_file = os.getenv('format_file')
            current_date = datetime.now()
            year, month, day, hour, minute, second = current_date.year, current_date.month, current_date.day, current_date.hour, current_date.minute, current_date.second
            if len(data[0]) != 0:
                name_file = f'{year}{str(month).zfill(2)}{str(day).zfill(2)}{str(hour).zfill(2)}{str(minute).zfill(2)}{str(second).zfill(2)}_U500Insight_{data[0]}.{format_file}'
            else:
                name_file = f'{year}{str(month).zfill(2)}{str(day).zfill(2)}{str(hour).zfill(2)}{str(minute).zfill(2)}{str(second).zfill(2)}_U500Insight.{format_file}'
            path_write_file = os.path.join(path_folder_to_write, name_file)

            parsed_date = datetime.strptime(data[2], "%m-%d-%Y %H:%M:%S")
            formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

            dict = {'id': "000000", 'merk': 'U500 Insight', 'date': formatted_date, 'parameter': []}
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
        except Exception as e:
            print('Error in writing data')
            print(e)

    def write_log(self, teks: str, string_json: dict):
        try:
            path_logs = os.getenv('path_logs')
            path_type_logs = os.getenv('path_logs_u500')
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

    def cleansing_and_retrieve_data_in_agd(self, result):
        # AMBIL DATA BERDASARKAN KATEGORI
        # PATTERN DATA ASCII
        patient_pattern = r'^ID:\s*([\d]*)\b'
        parameter_pattern = r'([*A-Z]{2,3}|pH|SG)\s+([\d+-.]*)\s*[a-zA-Z/]*?'
        # parameter_pattern = r'([*A-Za-z]+)\s+([\d+-.]*)\s+\w*\d*\/*'
        date_pattern = r'.*\s+([\d\-\:\s]*)\s+ID'

        # IMPLEMENTASI PATTERN DI ATAS
        patient_result = re.findall(pattern=patient_pattern, string=result)
        data_result = re.findall(pattern=parameter_pattern, string=result)
        date_result = re.findall(date_pattern, string=result)

        return (
            patient_result,
            data_result,
            date_result[0].strip()
        )

    def print_result(self, id, matches, date):
        alat_string = 'ALAT: U500Insight'
        waktu_string = f'WAKTU: {date}'
        id_string = f'ID: 00000'
        batas = "PARAMETER\t\tHASIL"

        all_text = f'{alat_string}\n{waktu_string}\n{id_string}\n{batas}\n'

        print(alat_string)
        print(waktu_string)

        # SIMPAN SEMENTARA
        # if id:
        #     print(f'ID: {id[0]}')
        # else:
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
            elif value == '-':
                note = 'nilai negatif'
            elif value == '+':
                note = 'nilai positif'
            elif value == '+-':
                note = 'trace'
            else:
                note = ''  # No additional note in this case
            updated_match = (parameter, value, note)
            updated_matches.append(updated_match)
        return updated_matches

    def ini_main(self, converted_data):
        try:
            identity, data_result, date = self.cleansing_and_retrieve_data_in_agd(result=converted_data)
            if identity or data_result and date:
                data_result = self.add_note(data_result)
                teks = self.print_result(identity, data_result, date)
                return [identity, data_result, date, teks]
            else:
                print("Bukan U500Insight")
        except Exception as e:
            print("Bukan U500Insight")

if __name__ == '__main__':
    try:
        list_file = []
        path_folder_to_read = 'transit_folder'
        path_folder_to_write = 'saved_data'
        while True:
            list_file = U500.listing_file(path_folder=path_folder_to_read)
            for file in list_file:
                if 'u500insight' in file.lower():
                    data, path_read_file = U500.processing_data(file, path_folder_to_read)
                    print(data)
                    U500.write_file(path_folder_to_write, data)
                    # os.remove(path_read_file)
            time.sleep(2)
            print('Kode berjalan')

    except Exception as e:
        print(e)