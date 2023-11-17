from Data import DHT22_Sensor, Email_Notification, SensorDatabase
import time
from datetime import datetime
import logging

#Schwellenwerte für die Warnung
temp_threshold_high = 22 # Grad Celsius
temp_threshold_low = 18 # Grad Celsius
temperature_email_msg = ""

#Setup des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Email Einstellungen
sender_adress ="Erik <test_email10@zohomail.eu>"
reciever_adress ="test_email10@zohomail.eu"
subject = "Betreff"

#ServerraumInfo
sensornummer = "Sensor (1)"

db_created = False

#Hauptprogramm
if __name__ == "__main__":
    try:
        #Instanzen erstellen
        sensor_instance = DHT22_Sensor()
        email_notifier = Email_Notification()
        db = SensorDatabase('SensorMessungen.db')
        
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
            #Datenbank Anlegen/erstellen
            if db_created == False:
                starttime_str = current_datetime.strftime('%X')
                db.delete_table()
                db.create_table()
                db_created = True
            #Temperatureabfrage durchführen
            if  f_temperature > temp_threshold_high:
                warning_printed = True
                db.insert_measurement(r_temperature, r_humidity, temp_plus_minus, temperature_deviation)
                db.export_to_csv()
                email_text = f"Hallo User, die Temperatur ist zu Hoch. Sie beträgt {r_temperature}°C."
                email_notifier.send_email("test_email10@zohomail.eu", "test_email10@zohomail.eu", f"Temperaturwarnung ({sensornummer})", email_text, "SensorMessungen.csv")

                #logger.warning(f"WARNUNG: Die Temperatur ist zu hoch! Sie beträgt {r_temperature}°C")
                #logger.info(f"Aktuelle Temperatur: {r_temperature}°C, Aktuelle Feuchtigkeit: {r_humidity}%")
            elif f_temperature < temp_threshold_low:
                warning_printed = True
                db.insert_measurement(r_temperature, r_humidity, temp_plus_minus, temperature_deviation)
                db.export_to_csv()
                email_text = f"Hallo User, die Temperatur ist zu Niedrig. Sie beträgt {r_temperature}°C."
                email_notifier.send_email("test_email10@zohomail.eu", "test_email10@zohomail.eu", f"Temperaturwarnung ({sensornummer})", email_text, "SensorMessungen.csv")

                #logger.warning(f"WARNUNG: Die Temperatur ist zu niedrig! Sie beträgt {r_temperature}°C")
                #logger.info(f"Aktuelle Temperatur: {r_temperature}°C, Aktuelle Feuchtigkeit: {r_humidity}%")                    
            else:
                db.insert_measurement(r_temperature, r_humidity, temp_plus_minus, temperature_deviation)
                db.export_to_csv()
            
            #Test in der Console
            print(f"Aktuelle Temperatur: {r_temperature}°C (Exakt: {temperature}°C)")
            print(f"Aktuelle Feuchtigkeit: {r_humidity}% (Exakt: {humidity}%)")
            endtime_str = current_datetime.strftime('%X')
            print(f"------------------{starttime_str}------------------Durchlauf Fertig!----------{endtime_str}---------------------------")

            time.sleep(60)  # Warte 60 Sekunden zwischen den Messungen
            

    except KeyboardInterrupt:
        logger.info("Programm beendet.")
    except Exception as e:
        logger.error(f"Ein Fehler ist aufgetreten: {e}")