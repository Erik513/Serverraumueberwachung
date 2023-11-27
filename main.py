from Data import DHT22_Sensor, Email_Notification, SensorDatabase
import time
from datetime import datetime
import logging

#Setup des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Schwellenwerte für die Warnung
temp_threshold_high = 22 # Grad Celsius
temp_threshold_low = 18 # Grad Celsius

#Email Einstellungen
sender_adress ="Erik <test_email10@zohomail.eu>"
reciever_adress ="test_email10@zohomail.eu"
subject = "Betreff"

#Email Spam Schutz
last_warning_time = None
warning_interval = 5 * 60  # 5 Minuten

#Intervall der Sensordaten
get_sensor_data_interval = 60 # 1 Min

#ServerraumInfo
sensornummer = "Sensor (1)"

#Booleans
db_DHT22_created = False
current_data_sended = False

#Hauptprogramm
if __name__ == "__main__":
    try:
        #Instanzen erstellen
        sensor_instance = DHT22_Sensor()
        email_notifier = Email_Notification()
        db_DHT22 = SensorDatabase('SensorMessungen.db')
        
        while True:
            #Datum
            current_datetime = datetime.now()
            date_str = current_datetime.strftime('%d.%m.%Y')
            #Lesen der Sensordaten
            temperature = sensor_instance.read_temperature()
            humidity = sensor_instance.read_humidity()
            #Runden
            r_temperature = "%.2f" % temperature
            r_humidity = "%.2f" % humidity
            #Umwandeln in float
            f_temperature = float(r_temperature)
            #Temperatur auswerten
            temp_plus_minus = sensor_instance.get_temperature_deviation_plus_minus(f_temperature, temp_threshold_low, temp_threshold_high)
            temperature_deviation = sensor_instance.get_temperature_deviation(f_temperature, temp_threshold_low, temp_threshold_high)
            #PDF-Passwort
            password = db_DHT22.generate_password()

            current_temperature = f"Aktuelle Temperatur: {r_temperature}°C (Exakt: {temperature}°C)"
            current_humidity = f"Aktuelle Feuchtigkeit: {r_humidity}% (Exakt: {humidity}%)"
            
            print(current_temperature)
            print(current_humidity)

            #Datenbank Anlegen/erstellen
            if not db_DHT22_created:
                date_str = current_datetime.strftime('%d.%m.%Y')
                starttime_str = current_datetime.strftime('%X')
                #db_DHT22.delete_table()
                db_DHT22.create_table()
                db_DHT22_created = True
            
            db_DHT22.insert_measurement(r_temperature, r_humidity, temp_plus_minus, temperature_deviation)

            if current_data_sended == False:
                current_date = current_datetime.strftime('%d.%m.%Y (%X)')
                message_text = f"Hallo User, im Anhang sind die aktuellen Daten zu finden." 
                #Mehrzeiliger Text
                email_text = f"""
                {message_text}

                Stand: {current_date}
                Erstellung der Datenbank: {date_str}, {starttime_str}
                Zulässige Temperaturen: {temp_threshold_low} - {temp_threshold_high} °C
                Momentane Luftfeuchtigkeit: {r_humidity} %
                Momentane Temperatur: {r_temperature} °C
                Temperaturabweichung in °C (falls vorhanden): {temp_plus_minus} {temperature_deviation}
                
                Passwort für die PDF-Datei: {password}
                """
                db_DHT22.export_to_csv()
                db_DHT22.create_pdf(password)
                db_DHT22.create_excel()
                email_notifier.send_email("test_email10@zohomail.eu", "test_email10@zohomail.eu", f"Aktuelle Daten ({sensornummer})", email_text, "SensorMessungen.csv", "SensorMessungen.pdf", "SensorMessungen.xlsx")
                current_data_sended = True

            #Temperatureabfrage durchführen
            if  f_temperature > temp_threshold_high:
                if last_warning_time is None or (current_datetime - last_warning_time).total_seconds() > warning_interval:
                    last_warning_time = current_datetime
                    
                    message_text = f"Hallo User, die Temperatur ist zu Hoch. Sie beträgt {r_temperature}°C."
                    #Mehrzeiliger Text
                    email_text = f"""
                    {message_text}

                    Stand: {current_date}
                    Erstellung der Datenbank: {date_str}, {starttime_str}
                    Zulässige Temperaturen: {temp_threshold_low} - {temp_threshold_high} °C
                    Momentane Luftfeuchtigkeit: {r_humidity} %
                    Momentane Temperatur: {r_temperature} °C
                    Temperaturabweichung in °C (falls vorhanden): {temp_plus_minus} {temperature_deviation}
                    
                    Passwort für die PDF-Datei: {password}
                    """
                    db_DHT22.export_to_csv()
                    db_DHT22.create_pdf(password)
                    db_DHT22.create_excel()
                    email_notifier.send_email("test_email10@zohomail.eu", "test_email10@zohomail.eu", f"Temperaturwarnung ({sensornummer})", email_text, "SensorMessungen.csv", "SensorMessungen.pdf", "SensorMessungen.xlsx")
                else:
                    print(f"Email wurde bereits verschickt: {last_warning_time}")
            
            elif f_temperature < temp_threshold_low:
                if last_warning_time is None or (current_datetime - last_warning_time).total_seconds() > warning_interval:
                    last_warning_time = current_datetime
                    message_text = f"Hallo User, die Temperatur ist zu Niedrig. Sie beträgt {r_temperature}°C."
                    #Mehrzeiliger Text
                    email_text = f"""
                    {message_text}

                    Stand: {current_date}
                    Erstellung der Datenbank: {date_str}, {starttime_str}
                    Zulässige Temperaturen: {temp_threshold_low} - {temp_threshold_high} °C
                    Momentane Luftfeuchtigkeit: {r_humidity} %
                    Momentane Temperatur: {r_temperature} °C
                    Temperaturabweichung in °C (falls vorhanden): {temp_plus_minus} {temperature_deviation}
                    
                    Passwort für die PDF-Datei: {password}
                    """
                    db_DHT22.export_to_csv()
                    db_DHT22.create_pdf(password)
                    db_DHT22.create_excel()
                    email_notifier.send_email("test_email10@zohomail.eu", "test_email10@zohomail.eu", f"Temperaturwarnung ({sensornummer})", email_text,"SensorMessungen.csv", "SensorMessungen.pdf", "SensorMessungen.xlsx")
                    print(f"Email wurde bereits verschickt: {last_warning_time}")

            #Test in der Console
            endtime_str = current_datetime.strftime('%X')
            print(f"------------------{starttime_str}------------------Durchlauf Fertig!----------{endtime_str}---------------------------")
            time.sleep(get_sensor_data_interval)  # Warte 60 Sekunden zwischen den Messungen
    
    except KeyboardInterrupt: 
        logger.info("Programm beendet") 
    except Exception as e:
        logger.error(f"EinFehler ist aufgetreten: {e}")