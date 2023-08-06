import os.path
import sys
import json

from excel_to_json.workbook import WorkBook
from excel_to_json.date_encoder import DateEncoder


def convert_xlsl(excel_file):
    file_dir = os.path.dirname(excel_file)
    workbook = WorkBook()
    workbook.load_file(excel_file)
    json_datas = workbook.json_datas
    for file_name, json_data in json_datas:
        f = open(os.path.join(file_dir, file_name), 'w+', encoding='utf-8')
        f.write(json.dumps(json_data, cls=DateEncoder, ensure_ascii=False))
        f.close()
        print('%s generated succeed.' % file_name)


def convert_folder(folder_path):
    paths = os.listdir(folder_path)
    for path in paths:
        if os.path.isdir(path):
            convert_folder(path)
        elif os.path.isfile(path) and path.endswith('.xlsx'):
            convert_xlsl(path)


def excel_to_json():
    input_paths = sys.argv[1:]
    for path in input_paths:
        if os.path.isdir(path):
            convert_folder(path)
        elif os.path.isfile(path) and path.endswith('.xlsx'):
            convert_xlsl(path)
