import sqlite3
import csv
from datetime import datetime
#csv
from cryptography.fernet import Fernet
#pdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
#excel
import openpyxl
from openpyxl.utils import get_column_letter

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
                    Problem TEXT,
                    Differenz TEXT
                )
            ''')
            cursor.execute('SELECT Datum FROM SensorMessungen WHERE ID = 1')
            first_date_in_db = cursor.fetchone()
            cursor.execute('SELECT Uhrzeit FROM SensorMessungen WHERE ID = 1')
            first_time_in_db = cursor.fetchone()
            if first_date_in_db and first_time_in_db:
                return f"Erstellung der Datenbank: {first_date_in_db[0]} {first_time_in_db[0]}"
            else:
                return None

    def insert_measurement(self, r_temperature, r_humidity, temp_plus_minus, temperature_deviation):
        current_datetime = datetime.now()
        date_str = current_datetime.strftime('%d.%m.%Y')
        time_str = current_datetime.strftime('%X')

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO SensorMessungen (Datum, Uhrzeit, Luftfeuchtigkeit, Temperatur_in_C°, Problem, Differenz)
                VALUES (? , ?, ?, ?, ?, ?)
            ''', (date_str, time_str, r_humidity, r_temperature, temp_plus_minus, temperature_deviation))

    def export_to_csv(self, csv_filename="SensorMessungen.csv"):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM SensorMessungen')
            rows = cursor.fetchall()
            if rows:
                header = [description[0] for description in cursor.description]
                # Schreiben Sie die Daten in die CSV-Datei
                with open(csv_filename, 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(header)
                    csv_writer.writerows(rows)

                print(f'Datenbank erfolgreich in verschlüsselter CSV exportiert: {csv_filename}')
            else:
                print('Die Datenbank ist leer. Keine CSV-Datei erstellt.')

    def get_all_measurements(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM SensorMessungen')
            return cursor.fetchall()
    
    @staticmethod
    def generate_password():
        import random
        import string
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for _ in range(6))
        return password
    
    def create_pdf(self, password):        
        data = self.get_all_measurements()
        pdf_filename = "SensorMessungen.pdf"

        #Erstellen Sie das PDF-Dokument mit Verschlüsselung    
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter, encrypt=password)
        elements = []
        styles = getSampleStyleSheet()

        #Fügen Sie einen Titel hinzu
        current_date = current_datetime.strftime('%d.%m.%Y (%X)')
        title_text = f"<u>Sensormessungen</u><br/><font size='8'>Stand: <font size='8' color='blue'>{current_date}</font></font>"
        title = Paragraph(title_text, styles['Title'])
        elements.append(title)

        elements.append(Spacer(1, 12))

        #Fügen Sie zusätzlichen Text mittig über der Tabelle hinzu
        additional_text = f"{SensorDatabase.create_table(self)}"
        text = Paragraph(additional_text, styles['Normal'])
        elements.append(text)

        # Fügen Sie eine leere Fläche in der Mitte des Dokuments hinzu
        elements.append(Spacer(1, doc.height / 16))

        # Erstellen Sie eine Tabelle und fügen Sie Daten hinzu
        header = ["ID", "Datum", "Uhrzeit", "Luftfeuchtigkeit in %", "Temperatur in C°", "Problem", "Differenz"]
        table_data = [header] + [list(map(str, row)) for row in data]
        table = Table(table_data)

        # Fügen Sie Gridlines zur Tabelle hinzu
        style = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        # Fügen Sie die Tabelle zum PDF hinzu
        elements.append(table)

        # Erstellen Sie das PDF-Dokument
        doc.build(elements)

        print(f'Datenbank erfolgreich in PDF exportiert: {pdf_filename}')
        return pdf_filename

    def create_excel(self, excel_filename="SensorMessungen.xlsx"):
        data = self.get_all_measurements()
        
        # Erstellen Sie eine neue Arbeitsmappe
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Schreiben Sie die Überschriften
        header = ["ID", "Datum", "Uhrzeit", "Luftfeuchtigkeit in %", "Temperatur in C°", "Problem", "Differenz"]
        sheet.append(header)

        # Holen Sie alle Messungen aus der Datenbank
        data = self.get_all_measurements()

        # Schreiben Sie die Daten in die Tabelle
        for row in data:
            sheet.append(row)

        # Passen Sie die Spaltenbreite basierend auf dem Header an
        for col_num, column_title in enumerate(header, 1):
            col_letter = get_column_letter(col_num)
            max_length = 0
            for cell in sheet[col_letter]:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[col_letter].width = adjusted_width

        # Speichern Sie die Excel-Datei
        workbook.save(excel_filename)

        print(f'Datenbank erfolgreich in Excel exportiert: {excel_filename}')
        return excel_filename

    def delete_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE SensorMessungen')