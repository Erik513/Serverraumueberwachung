from Data import DHT22_Sensor, Email_Notification
import time

temperature = DHT22_Sensor.read_temperature()
r_temperature = "%.2f" % temperature

humidity = DHT22_Sensor.read_humidity()

# Schwellenwerte für die Warnung
temp_threshold_high = 22 # Grad Celsius
temp_threshold_low = 18 # Grad Celsius
temperature_string = ""
#Hauptprogramm
if __name__ == "__main__":
    try:
        while True:

            if temperature > temp_threshold_high:
                print(f"WARNUNG: Die Temperatur ist zu hoch! Sie beträgt {temperature}°C")
                print(f"Aktuelle Temperatur: {temperature}°C")
                print(f"Aktuelle Feuchtigkeit: {humidity}%")
                temperature_string = f"Temperatur ist zu Hoch. Sie Beträgt {r_temperature}°C"
                Email_Notification.send_notification(temperature_string)
            elif temperature < temp_threshold_low:
                print(f"WARNUNG: Die Temperatur ist zu niedrig! Sie beträgt {temperature}°C")
                temperature_string = f"Temperatur ist zu niedrig. Sie Beträgt {temperature}°C"
                Email_Notification.send_notification(temperature_string)
            time.sleep(10)  # Warte 10 Sekunden zwischen den Messungen

    except KeyboardInterrupt:
        print("Programm beendet.")