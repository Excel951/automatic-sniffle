import re
import os
from .utils import convert
from .utils import retrieve_data as rd

# FINISHED

def cleansing_and_retrieve_data_xn1000(result):
    # PATTERN DATA ASCII
    # DATA                          R/0/P/H|NUM |^^^param | FIELD PARAMETER              | NUM ^^ |
    pattern_parameter_in_xn1000 = r"R\|\d+\|\^{4}([\w\%\#\-]+)\^*\d+\|([\d+\.\-]+)"

    # AMBIL DATA YANG DIPERLUKAN
    # DATA
    matches = re.findall(pattern=pattern_parameter_in_xn1000, string=result)

    return matches

def print_result(matches):
    print("Result XN1000")
    for match in matches:
        parameter, value = match
        print(f'Parameter: {parameter}, Nilai: {value}')

def ini_main(converted_data):
    try:
        matches = cleansing_and_retrieve_data_xn1000(converted_data)
        if matches:
            print_result(matches)
            return matches
        else:
            print("Bukan XN1000")
    except Exception as e:
        print("Bukan XN1000")

if __name__ == '__main__':
    name_file = "HEXA_XN1000_20240514_11-55.log.txt"
    # name_file = "CHARC_XN1000_20240514_11-55.log.txt"
    parent_file_path = os.path.join('../files_hexa', name_file)

    hexa_content = rd.retrieve_data_read_only(parent_file_path)
    result = convert.convert_hexa_to_ascii(hexa_content=hexa_content)
    matches = cleansing_and_retrieve_data_xn1000(result=result)
    print_result(matches)