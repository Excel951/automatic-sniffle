import os
import time

from dotenv import load_dotenv

from WONDFOBGA import WONDFOBGA
from EXIAS import Exias
from XN1000 import XN1000
from AGD import AGD
from PROMED import PROMED
from U500 import U500

load_dotenv()

def register_file(path_folder):
    list_file = [file for file in os.listdir(path_folder)]
    return list_file

# TUGAS MENCOCOKKAN HASIL SESUAI DENGAN JSON YANG DIBERIKAN
if __name__ == '__main__':
    try:
        Xn1000 = XN1000()
        Agd = AGD()
        exias = Exias()
        Promed = PROMED()
        U500 = U500()
        Wond = WONDFOBGA()

        list_file = []
        path_folder_to_read = os.getenv('path_folder_to_read')
        path_folder_to_write = os.getenv('path_folder_to_write')
        read_file = False
        while True:
            list_file = register_file(path_folder=path_folder_to_read)
            for file in list_file:

                if 'xn1000' in file.lower():
                    data, id, path_read_file, date, teks = Xn1000.processing_data(file=file, path_folder_to_read=path_folder_to_read)
                    Xn1000.write_file(path_folder_to_write, data, id, date, teks)
                    read_file = True

                elif 'agd' in file.lower():
                    data, path_read_file = Agd.processing_data(file, path_folder_to_read)
                    Agd.write_file(path_folder_to_write, data)
                    read_file = True

                elif 'exias' in file.lower():
                    data, path_read_file = exias.processing_data(file=file, path_folder_to_read=path_folder_to_read)
                    exias.write_file(path_folder_to_write, data)
                    read_file = True

                elif 'promed' in file.lower():
                    data, path_read_file = Promed.processing_data(file=file, path_folder_to_read=path_folder_to_read)
                    Promed.write_file(path_folder_to_write, data)
                    read_file = True

                elif 'u500insight' in file.lower():
                    data, path_read_file = U500.processing_data(file=file, path_folder_to_read=path_folder_to_read)
                    U500.write_file(path_folder_to_write, data)
                    read_file = True

                elif 'wondfobga' in file.lower():
                    data, path_read_file = Wond.processing_data(file=file, path_folder_to_read=path_folder_to_read)
                    Wond.write_file(path_folder_to_write, data)
                    read_file = True

                if read_file:
                    # DELETE FILE
                    os.remove(path_read_file)
                    read_file = False
                    print("\nRetrieve Data Done")

            time.sleep(0.5)
    except Exception as e:
        print(e)