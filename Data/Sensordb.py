import sqlite3
import csv
import io
from datetime import datetime
from Data import DHT22_Sensor

#Datum
current_datetime = datetime.now()

class SensorDatabase: 

    def __init__(self, db_name="SensorMessungen.csv"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS SensorMessungen (
                    ID INTEGER PRIMARY KEY,
                    Datum DATETIME,
                    Uhrzeit TEXT,
                    Luftfeuchtigkeit REAL,
                    Temperatur_in_C° REAL,
                    Fehler TEXT,
                    Differenz TEXT
                )
            ''')

    def insert_measurement(self, r_temperature, r_humidity, temp_plus_minus, temperature_deviation):
        current_datetime = datetime.now()
        date_str = current_datetime.strftime('%d.%m.%Y')
        time_str = current_datetime.strftime('%X')

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO SensorMessungen (Datum, Uhrzeit, Luftfeuchtigkeit, Temperatur_in_C°, Fehler, Differenz)
                VALUES (? , ?, ?, ?, ?, ?)
            ''', (date_str, time_str, r_humidity, r_temperature, temp_plus_minus, temperature_deviation))

    def export_to_csv(self, csv_filename="SensorMessungen.csv"):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM SensorMessungen')

            rows = cursor.fetchall()

            if rows:
                header = [description[0] for description in cursor.description]

                with open(csv_filename, 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(header)
                    csv_writer.writerows(rows)

                print(f'Datenbank erfolgreich in CSV exportiert: {csv_filename}')
            else:
                print('Die Datenbank ist leer. Keine CSV-Datei erstellt.')
    
    def delete_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE SensorMessungen')