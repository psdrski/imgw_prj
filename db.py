import requests

''' funkcja tworzaca liste zawierajaca id wszystkich stacji w API'''

def create_list():
    var = requests.get(f'https://danepubliczne.imgw.pl/api/data/synop')
    data = var.json()

    id_list = [atr.get('id_stacji') for atr in data]
    return id_list

