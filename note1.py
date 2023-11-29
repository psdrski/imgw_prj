import psycopg2
from configparser import ConfigParser
from datetime import datetime

temp = 20.5
cisnienie = 1013.2
suma_opadu = 5.0
predkosc_wiatru = 15.0
time = datetime.now()
id_ = 3

def config(filename="login.ini", section="postgresql"):
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




def connect():
    connection = None
    cur = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        cur = connection.cursor()

        cur.execute("""
                    INSERT INTO db.dane(
                        temp, cisnienie, suma_opadu, predkosc_wiatru, "time", id_)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (temp, cisnienie, suma_opadu, predkosc_wiatru, time, id_))

        connection.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            cur.close()
            connection.close()
            print('end')



connect()




