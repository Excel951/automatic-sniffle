import os

def retrieve_data_read_only(path_file):
    # RETRIEVE FILE HEX
    with open(path_file, "r") as file:
        hexa_content = file.read()
    return hexa_content