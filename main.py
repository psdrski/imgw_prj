from functions import start

def main():

    print('1 - Pobieranie danych pogodowych')
    print('2 - Utworzenie tabeli stacji')
    print('3 - Utworzenie gpkg')
    x = input('Wybierz funkcje')

    _start = start()
    if x == '1':
        _start.synop_data()
    if x == '2':
        _start.station_data()
    elif x == '3':
        n = input('podaj nazwę pliku')
        _start.prepare_gpkg_from(output_name=n)

if __name__ == '__main__':
    main()
