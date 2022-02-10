import json

def file_to_json(path):
    result = {}
    with open(path, encoding='utf-8') as data_file:
        result = json.load(data_file)
    return result

def json_to_file(path, json_data):
    with open(path, 'w', encoding='utf-8') as data_file:
        json.dump(json_data, data_file, indent=2, ensure_ascii=False)
    pass