import re
from .utils import retrieve_data as rd
from .utils import convert

# import sys
# import os
#
# # Tambahkan path dari direktori parent ke sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# FINISHED

def cleansing_and_retrieve_data_in_agd(data_in_ascii):
    # CLEAN ALL NON PRINTABLE
    file_ascii = data_in_ascii.replace('', '')

    # AMBIL DATA BERDASARKAN KATEGORI
    # PATTERN DATA ASCII
    patient_pattern = r'Patient ID:\|*\s*(\d+)'
    acid_base_pattern = r'(pH\s+\d+\.\d+[\s\S]+?stHCO3\s+\d+\.\d+\s+mmol/L)'
    hemoglobin_oxygen_pattern = r'(tHb\s+\d+\.\d+\s+g/dL[\s\S]+?O2Ct\s+\d+\.\d+\s+%vol)'

    # IMPLEMENTASI PATTERN DI ATAS
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
        patient_result,
        data_acid,
        data_hemoglobin_oxygen
    )

def print_result(id, matches):
    print('AGD')
    print(f'Patient ID: {id[0]}')
    # DATA ACID
    print(f'\nACID/BASE')
    for match in matches[0]:
        param, value = match
        print(f'{param}:\t\t{value}')

    print(f'\nHEMOGLOBIN/OXGEN STATUS')
    for match in matches[1]:
        parameter, value = match
        print(f'{parameter}:\t\t{value}')

def ini_main(converted_data):
    try:
        identity, data_acid, data_hemoglobin_oxygen = cleansing_and_retrieve_data_in_agd(data_in_ascii=converted_data)
        if identity and data_acid and data_hemoglobin_oxygen:
            print_result(identity, matches=(data_acid, data_hemoglobin_oxygen))
            return (identity, data_acid, data_hemoglobin_oxygen)
        else:
            print("Bukan AGD")
    except Exception as e:
        print("Bukan AGD")
    # return {
    #     id: identity,
    #     data_acid: data_acid,
    #     data_hemoglobin_oxygen: data_hemoglobin_oxygen
    # }

if __name__ == '__main__':
    name_file = "HEXA_AGD_20240129_04-57.log.txt"
    parent_file_path = os.path.join("../files_hexa/", name_file)
    hexa_content = rd.retrieve_data_read_only(path_file=parent_file_path)
    result = convert.convert_hexa_to_ascii(hexa_content=hexa_content)

    identity, data_acid, data_hemoglobin_oxygen = cleansing_and_retrieve_data_in_agd(data_in_ascii=result)

    print_result(identity, matches=(data_acid, data_hemoglobin_oxygen))