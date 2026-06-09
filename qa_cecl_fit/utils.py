import pyperclip
import os
import const

def get_data_from_clipboard():
    data =  pyperclip.paste()
    data = data.replace('\r\n', '\n')

    #first blank line remove
    data = data.lstrip('\n')
    return data

def write_file(file_path,data):
    with open(file_path,"w",newline='') as f:
        f.write(data)

def check_file_exists(file_path):
    return os.path.isfile(file_path)

def get_files_config(full_path):
    for file_config in file_config_generator(full_path):
        file_path = file_config.get('full_path')
        if not check_file_exists(file_path):
            yield file_config

def file_config_generator(full_path):
    for file_config in const.ALL_FILES:
        # if file_config.get('report_id',0)>30:
        file_name = file_config.get('file_name')
        file_with_path = os.path.join(full_path,file_name)
        file_config['full_path'] = file_with_path
        yield file_config
