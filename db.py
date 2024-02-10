import requests

''' funkcja tworzaca liste zawierajaca id wszystkich stacji w API'''

def create_id_list():
    var = requests.get(f'https://danepubliczne.imgw.pl/api/data/synop')
    data = var.json()

    id_list = [atr.get('id_stacji') for atr in data]
    return id_list

def create_name_list():
    var = requests.get(f'https://danepubliczne.imgw.pl/api/data/synop')
    data = var.json()

    name_list = [atr.get('stacja') for atr in data]
    return name_list