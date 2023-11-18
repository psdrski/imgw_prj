import requests
from db import id_list


class measure_point:

    '''atrybuty'''

    def __init__(self, temperatura, cisnienie, suma_opadow, predkosc_wiatru, nazwa_msc):
        self.temperatura = temperatura
        self.cisnienie = cisnienie
        self.suma_opadow = suma_opadow
        self.predkosc_wiatru = predkosc_wiatru
        self.nazwa_msc = nazwa_msc


    '''funkcja pokazujaca atrybuty dla danej klasy'''

    def show_atr(self):
        print(self.temperatura, self.cisnienie, self.suma_opadow)



'''petla do odliczania po miejscowosciach w db'''

for id in id_list:


    '''pobranie json z serwisu'''

    var = requests.get(f'https://danepubliczne.imgw.pl/api/data/synop/id/{id}')
    data = var.json()

    print(data)

    '''dodanie wartosci atrybutow z json do zmiennych'''

    temperatura1 = float(var.json().get('temperatura'))
    cisnienie1 = float(var.json().get('cisnienie')) if var.json().get('cisnienie') is not None else None
    suma_opadu1 = float(var.json().get('suma_opadu'))
    predkosc_wiatru1 = float(var.json().get('predkosc_wiatru'))
    nazwa_msc1 = str(var.json().get('stacja'))

    '''aktualna zmienna ---> atrybuty + print atrybutow'''

    current = measure_point(temperatura1, cisnienie1, suma_opadu1, predkosc_wiatru1, nazwa_msc1)

    current.show_atr()

    '''ocena warunkow'''

    if temperatura1 > -20 and cisnienie1 is not None and cisnienie1 > 980 and suma_opadu1 < 10 and predkosc_wiatru1 < 100:
        print('ok')
    else:
        print('nie ok')

