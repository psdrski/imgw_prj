import requests

''' funkcja ktora pobiera dane z API za pomoca id stacji'''

def downl_data(id):
    var = requests.get(f'https://danepubliczne.imgw.pl/api/data/synop/id/{id}')
    data = var.json()
    print(data)
    return var


''' utworzenie klasy'''

class measure_point:

    ''' inicjowanie klasy, nadaje atrybuty '''

    def __init__(self, temperatura, cisnienie, suma_opadow, predkosc_wiatru, nazwa_msc):
        self.temperatura = temperatura
        self.cisnienie = cisnienie
        self.suma_opadow = suma_opadow
        self.predkosc_wiatru = predkosc_wiatru
        self.nazwa_msc = nazwa_msc


    ''' funkcja ukazujaca atrybuty dla danej klasy '''

    def show_atr(self):
        print(self.temperatura, self.cisnienie, self.suma_opadow, self.predkosc_wiatru)


    ''' funkcja ktora pobiera z pobranych wczeniej danych API wartosci dla atrybutow:
    jedna ze stacji nie podawala cisnienia, stad warunek if'''

    def add_atr(self, var):
        temperatura = float(var.json().get('temperatura'))
        cisnienie = float(var.json().get('cisnienie')) if var.json().get('cisnienie') is not None else None
        suma_opadow = float(var.json().get('suma_opadu'))
        predkosc_wiatru = float(var.json().get('predkosc_wiatru'))
        nazwa_msc = str(var.json().get('stacja'))

        self.temperatura = temperatura
        self.cisnienie = cisnienie
        self.suma_opadow = suma_opadow
        self.predkosc_wiatru = predkosc_wiatru
        self.nazwa_msc = nazwa_msc


    ''' funkcja porownujaca atrybuty danej stacji wzgledem okreslonych kryteriow'''

    def conditions(self):
        if \
                self.temperatura > -20 \
                and self.cisnienie is not None and self.cisnienie > 980 \
                and self.suma_opadow < 10 \
                and self.predkosc_wiatru < 100:
            print('ok')
        else:
            print('nie ok')




