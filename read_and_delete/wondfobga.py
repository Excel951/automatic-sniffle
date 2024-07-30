import json
import time
from datetime import datetime
from parse_data.utils import retrieve_data as rd
from parse_data.utils import convert as conv
from parse_data import wondfobga
import os

def listing_file(path_folder):
    list_file = [file for file in os.listdir(path_folder)]
    return list_file

def processing_data(file, path_folder_to_read):
    print(f'File name: {file}')
    path_read_file = os.path.join(path_folder_to_read, file)
    file = rd.retrieve_data_read_only(path_read_file)
    converted_data = conv.convert_hexa_to_ascii(file)
    data = wondfobga.ini_main(converted_data)
    datas = []
    for data in data:
        datas.append(data)
    return datas, path_read_file

def write_file(path_folder_to_write, data):
    current_date = datetime.now()
    year, month, day, hour, minute, second = current_date.year, current_date.month, current_date.day, current_date.hour, current_date.minute, current_date.second
    name_file = f'{year}-{month}-{day}_{hour}-{minute}-{second}_WONDFOBGA_{data[0]}_{data[1]}.txt'
    path_write_file = os.path.join(path_folder_to_write, name_file)

    dict = {'parameter': []}
    for i in range(len(data[2])):
        dict['parameter'].append({'parameter': data[2][i][0], 'nilai': data[2][i][1]})

    with open(path_write_file, 'w') as file:
        file.write(json.dumps(dict))

if __name__ == '__main__':
    try:
        list_file = []
        path_folder_to_read = 'transit_folder'
        path_folder_to_write = 'saved_data'
        while True:
            list_file = listing_file(path_folder=path_folder_to_read)
            for file in list_file:
                if 'wondfobga' in file.lower():
                    data, path_read_file = processing_data(file, path_folder_to_read)
                    print(data)
                    write_file(path_folder_to_write, data)
                    # os.remove(path_read_file)
            time.sleep(2)
            print('Kode berjalan')

    except Exception as e:
        print(e)