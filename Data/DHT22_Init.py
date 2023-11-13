import Adafruit_DHT

# Sensor-Typ (DHT22)
sensor = Adafruit_DHT.DHT22

# GPIO-Pin (4), an dem der Sensor angeschlossen ist
pin = 4

class DHT22_Sensor:
    # Funktion zur Temperaturmessung
    def read_temperature():
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        return temperature

    def read_humidity():
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        return humidity
        
