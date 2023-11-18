'''dodanie wartosci atrybutow z json do zmiennych'''

temperatura1 = float(var.json().get('temperatura'))
cisnienie1 = float(var.json().get('cisnienie'))
suma_opadu1 = float(var.json().get('suma_opadu'))
predkosc_wiatru1 = float(var.json().get('predkosc_wiatru'))

'''aktualna zmienna ---> atrybuty + print atrybutow'''

current = measure_point(temperatura1, cisnienie1, suma_opadu1, predkosc_wiatru1, msc)

current.show_atr()

'''ocena warunkow'''

if temperatura1 > -20 and cisnienie1 > 980 and suma_opadu1 < 10 and predkosc_wiatru1 < 100:
    print('ok')
else:
    print('nie ok')

    '''ocena warunkow'''

    if temperatura > -20 and cisnienie is not None and cisnienie > 980 and suma_opadu < 10 and predkosc_wiatru < 100:
        print('ok')
    else:
        print('nie ok')


