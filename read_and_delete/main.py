import os
import time

import xn1000
import agd
from read_and_delete import exias, promed, u500insight, wondfobga


def register_file(path_folder):
    list_file = [file for file in os.listdir(path_folder)]
    return list_file

if __name__ == '__main__':
    try:
        list_file = []
        path_folder_to_read = 'transit_folder'
        path_folder_to_write = 'saved_data'
        read_file = False
        while True:
            list_file = register_file(path_folder=path_folder_to_read)
            for file in list_file:
                if 'xn1000' in file.lower():
                    data, path_read_file = xn1000.processing_data(file=file, path_folder_to_read=path_folder_to_read)
                    xn1000.write_file(path_folder_to_write, data)
                    read_file = True
                if 'agd' in file.lower():
                    data, path_read_file = agd.processing_data(file, path_folder_to_read)
                    agd.write_file(path_folder_to_write, data)
                    read_file = True
                if 'exias' in file.lower():
                    data, path_read_file = exias.processing_data(file=file, path_folder_to_read=path_folder_to_read)
                    exias.write_file(path_folder_to_write, data)
                    read_file = True
                if 'promed' in file.lower():
                    data, path_read_file = promed.processing_data(file=file, path_folder_to_read=path_folder_to_read)
                    promed.write_file(path_folder_to_write, data)
                    read_file = True
                if 'u500insight' in file.lower():
                    data, path_read_file = u500insight.processing_data(file=file, path_folder_to_read=path_folder_to_read)
                    u500insight.write_file(path_folder_to_write, data)
                    read_file = True
                if 'wondfobga' in file.lower():
                    data, path_read_file = wondfobga.processing_data(file=file, path_folder_to_read=path_folder_to_read)
                    wondfobga.write_file(path_folder_to_write, data)
                    read_file = True
                if read_file:
                    os.remove(path_read_file)
                    read_file = False
            time.sleep(0.5)
    except Exception as e:
        print(e)