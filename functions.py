import requests
import geopandas as gpd
import pandas as pd

from datetime import datetime
from shapely.geometry import Point
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, DateTime, Numeric, Sequence, Text, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from db import create_id_list, create_name_list

# funkcja ktora pobiera dane z API za pomoca id stacji
def downl_data(id):
    var = requests.get(f'https://danepubliczne.imgw.pl/api/data/synop/id/{id}')
    data = var.json()
    print(data)
    return var


# utworzenie klasy dla rejestrow w pierwszej tabeli
class measure_point:

    # nadaje atrybuty punktu pomiarowego
    def __init__(self, temperatura, cisnienie, suma_opadow, predkosc_wiatru, id_stacji, nazwa_msc):
        self.temperatura = temperatura
        self.cisnienie = cisnienie
        self.suma_opadow = suma_opadow
        self.predkosc_wiatru = predkosc_wiatru
        self.id_stacji = id_stacji
        self.nazwa_msc = nazwa_msc


    # zwykly print
    def show_atr(self):
        print(self.temperatura, self.cisnienie, self.suma_opadow, self.predkosc_wiatru, self.nazwa_msc)


    ''' funkcja ktora pobiera z pobranych wczeniej danych API wartosci dla atrybutow:
    jedna ze stacji nie podawala cisnienia, stad warunek if'''

    def add_atr(self, var):
        temperatura = float(var.json().get('temperatura')) if var.json().get('temperatura') is not None else None
        cisnienie = float(var.json().get('cisnienie')) if var.json().get('cisnienie') is not None else None
        suma_opadow = float(var.json().get('suma_opadu'))
        predkosc_wiatru = float(var.json().get('predkosc_wiatru')) if var.json().get('predkosc_wiatru') is not None else None
        id_stacji = int(var.json().get('id_stacji'))
        nazwa_msc = str(var.json().get('stacja'))

        self.temperatura = temperatura
        self.cisnienie = cisnienie
        self.suma_opadow = suma_opadow
        self.predkosc_wiatru = predkosc_wiatru
        self.nazwa_msc = nazwa_msc
        self.id_stacji = id_stacji

        return(temperatura, cisnienie, suma_opadow, predkosc_wiatru, id_stacji, nazwa_msc)


    # funkcja porownujaca atrybuty danej stacji wzgledem okreslonych kryteriow
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



# definiowanie dwoch tabel
Base = declarative_base()
class tab1(Base):
    __tablename__ = 'tab1'
    __table_args__ = {'schema': 'db'}

    tab1_id = Column(Integer, Sequence('tab1_tab1_id_seq', schema='db'), primary_key=True)
    temp = Column(Numeric)
    cisnienie = Column(Numeric)
    suma_opadu = Column(Numeric)
    predkosc_wiatru = Column(Numeric)
    time = Column(DateTime)
    id_stacji = Column(Integer)
    nazwa_stacji = Column(Text)

class tab2(Base):
    __tablename__ = 'tab2'
    __table_args__ = {'schema': 'db'}

    tab2_id = Column(Integer, Sequence('tab2_tab2_id_seq', schema='db'), primary_key=True)
    nazwa_stacji = Column(Text, ForeignKey('db.tab1.nazwa_stacji'))
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    tab1 = relationship('tab1',uselist=False, foreign_keys=[nazwa_stacji])


class tab1_connection:
    def __init__(self):
        self.engine = create_engine(f"postgresql+psycopg2://postgres:sad1@localhost:5432/imgw_db")
        self.Session = sessionmaker(bind=self.engine)


    def connect(self, temp, cisnienie, suma_opadu, predkosc_wiatru, time, id_stacji, nazwa_stacji):
        session = self.Session()
        try:

            data_input = tab1(
                temp=temp,
                cisnienie=cisnienie,
                suma_opadu=suma_opadu,
                predkosc_wiatru=predkosc_wiatru,
                time=datetime.now(),
                id_stacji=id_stacji,
                nazwa_stacji=nazwa_stacji
            )

            session.add(data_input)
            session.commit()

        except Exception as error:
            print(error)
        finally:
            session.close()
            print('Koniec')


class tab2_connection:
    def __init__(self):
        self.engine = create_engine(f"postgresql+psycopg2://postgres:sad1@localhost:5432/imgw_db")
        self.Session = sessionmaker(bind=self.engine)


    def connect(self, nazwa_stacji, response_html_latitude, response_html_longitude):
        session = self.Session()
        try:

            data_input = tab2(
                nazwa_stacji=nazwa_stacji,
                latitude=response_html_latitude,
                longitude=response_html_longitude,
            )

            session.add(data_input)
            session.commit()

        except Exception as error:
            print(error)
        finally:
            session.close()
            print('Koniec')


# klasa pobierajaca wspolrzedne miejscowosci z listy, za pomoca wikipedii
class coordinates:
    def get_coordinates_of(city: str) -> list[float, float]:
        # pobranie stron internetowych
        adres_URL = f'https://pl.wikipedia.org/wiki/{city}'
        response = requests.get(url=adres_URL)
        response_html = BeautifulSoup(response.text, 'html.parser')

        # pobranie współrzędnych z treści strony internetowej
        response_html_latitude = response_html.select('.latitude')[1].text  # .  class
        response_html_latitude = float(response_html_latitude.replace(',', '.'))
        response_html_longitude = response_html.select('.longitude')[1].text  # .  class
        response_html_longitude = float(response_html_longitude.replace(',', '.'))

        return [response_html_latitude, response_html_longitude]


# klasa reprezentujaca rejestry w drugiej tabeli
class measure_point2:

    # inicjowanie klasy, nadaje atrybuty

    def __init__(self, nazwa_msc, latitude, longitude):
        self.nazwa_msc = nazwa_msc
        self.latitude = latitude
        self.longitude = longitude




# klasa ktora umozliwia operacje na tabelac
class start:

    def __init__(self):
        self.tab1_connection = tab1_connection()
        self.tab2_connection = tab2_connection()

    def synop_data(self):
        id_list = create_id_list()
        db_connection1 = tab1_connection()
        for id in id_list:
            var1 = downl_data(id)
            current = measure_point(0, 0, 0, 0, 0, "")
            current.add_atr(var1)
            current.show_atr()
            current.conditions()

            temperatura = current.temperatura
            cisnienie = current.cisnienie
            suma_opadow = current.suma_opadow
            predkosc_wiatru = current.predkosc_wiatru
            nazwa_stacji = current.nazwa_msc
            id_stacji = current.id_stacji
            time = datetime.now()

            db_connection1.connect(temperatura, cisnienie, suma_opadow, predkosc_wiatru, time, id_stacji, nazwa_stacji)

    def station_data(self):
        name_list = create_name_list()
        db_connection2 = tab2_connection()
        for n in name_list:
            try:
                var2 = coordinates.get_coordinates_of(n)

                current = measure_point2(n, var2[0], var2[1])
                print(f"Name: {n}")
                print(f"Coordinates: {var2}")

                db_connection2.connect(current.nazwa_msc, current.latitude, current.longitude)

            except:
                print(f"Nie można pobrać współrzędnych dla stacji {n}")
                continue

    def prepare_gpkg_from(self, output_name: str) -> None:
        connection = "postgresql://postgres:sad1@localhost:5432/imgw_db"
        engine = create_engine(connection)

        Session = sessionmaker(bind=engine)
        session = Session()
        # posrednie zapytanie, sortujace rejestry wzgledem najnowszej daty
        _subquery = session.query(tab1.nazwa_stacji, func.max(tab1.time).label("latest_time")).group_by(
            tab1.nazwa_stacji).subquery()
        # glowne zapytanie, grupujące 3 atrybuty z tab2 i 2 z tab1
        _query = session.query(tab2.latitude, tab2.longitude, tab2.nazwa_stacji, tab1.temp, tab1.time). \
            join(tab1).filter(tab2.nazwa_stacji == tab1.nazwa_stacji).filter(tab1.time == _subquery.c.latest_time)

        # wykonanie zapytania i zapis do zmiennej dataframe
        df = pd.read_sql_query(_query.statement, engine)

        session.close()

        # tworzenie geometrii z atrybutow lng i lat
        # zip iteruje po dwoch listach jednoczesnie i laczy te elementy ze soba
        geometry = [Point(lon, lat) for lon, lat in zip(df['longitude'], df['latitude'])]

        # dataframe z geometrią
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

        # zapis do pliku
        gdf.to_file(f'{output_name}.gpkg', driver='GPKG')

