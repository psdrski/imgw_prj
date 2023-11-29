import requests
import psycopg2
from configparser import ConfigParser
from datetime import datetime

''' funkcja ktora pobiera dane z API za pomoca id stacji'''

def downl_data(id):
    var = requests.get(f'https://danepubliczne.imgw.pl/api/data/synop/id/{id}')
    data = var.json()
    print(data)
    return var


''' utworzenie klasy'''

class measure_point:

    ''' inicjowanie klasy, nadaje atrybuty '''

    def __init__(self, temperatura, cisnienie, suma_opadow, predkosc_wiatru, nazwa_msc, id_stacji):
        self.temperatura = temperatura
        self.cisnienie = cisnienie
        self.suma_opadow = suma_opadow
        self.predkosc_wiatru = predkosc_wiatru
        self.nazwa_msc = nazwa_msc
        self.id_stacji = id_stacji


    ''' funkcja ukazujaca atrybuty dla danej klasy '''

    def show_atr(self):
        print(self.temperatura, self.cisnienie, self.suma_opadow, self.predkosc_wiatru)


    ''' funkcja ktora pobiera z pobranych wczeniej danych API wartosci dla atrybutow:
    jedna ze stacji nie podawala cisnienia, stad warunek if'''

    def add_atr(self, var):
        temperatura = float(var.json().get('temperatura')) if var.json().get('temperatura') is not None else None
        cisnienie = float(var.json().get('cisnienie')) if var.json().get('cisnienie') is not None else None
        suma_opadow = float(var.json().get('suma_opadu'))
        predkosc_wiatru = float(var.json().get('predkosc_wiatru')) if var.json().get('predkosc_wiatru') is not None else None
        nazwa_msc = str(var.json().get('stacja'))
        id_stacji = int(var.json().get('id_stacji'))

        self.temperatura = temperatura
        self.cisnienie = cisnienie
        self.suma_opadow = suma_opadow
        self.predkosc_wiatru = predkosc_wiatru
        self.nazwa_msc = nazwa_msc
        self.id_stacji = id_stacji

        return(temperatura, cisnienie, suma_opadow, predkosc_wiatru, id_stacji)


    ''' funkcja porownujaca atrybuty danej stacji wzgledem okreslonych kryteriow'''

    def conditions(self):
        if (
                self.temperatura > -20
                and self.cisnienie is not None and self.cisnienie > 980
                and self.suma_opadow < 10
                and self.predkosc_wiatru is not None and self.predkosc_wiatru < 100
        ):
            print('ok')
        else:
            print('nie ok')


'''klasa odpowiadajaca za interakcje z db w sql'''
class db_connection:
    '''łączenie z db, wpis danych do tabeli'''
    def connect(self, temp, cisnienie, suma_opadu, predkosc_wiatru, time, id_stacji):
        connection = None
        cur = None
        try:
            params = self.config()
            connection = psycopg2.connect(**params)
            cur = connection.cursor()

            db_id = self.get_next_db_id(cur)

            self.input(cur, db_id, temp, cisnienie, suma_opadu, predkosc_wiatru, time, id_stacji)

            connection.commit()

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                if cur is not None:
                    cur.close()
                connection.close()
                print('end')


    def get_next_db_id(self, cur):
        cur.execute("SELECT nextval('db.new_id')")
        db_id = cur.fetchone()[0]
        return db_id

    def input(self, cur, db_id, temp, cisnienie, suma_opadu, predkosc_wiatru, time, id_stacji):

        cur.execute("""
                        INSERT INTO db.dane(
                            db_id, temp, cisnienie, suma_opadu, predkosc_wiatru, "time", id_stacji)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (db_id, temp, cisnienie, suma_opadu, predkosc_wiatru, time, id_stacji))



    def config(self, filename="login.ini", section="postgresql"):
        parser = ConfigParser()
        parser.read(filename)
        login = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                login[param[0]] = param[1]
                print(login)
        else:
            print('niepoprawne dane w pliku logowania')

        return login
