import requests

var = requests.get(f'https://danepubliczne.imgw.pl/api/data/synop')
data = var.json()

id_list = [atr.get('id_stacji') for atr in data]

