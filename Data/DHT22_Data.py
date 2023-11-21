import Adafruit_DHT

# Sensor-Typ (DHT22)
sensor = Adafruit_DHT.DHT22

# GPIO-Pin (4), an dem der Sensor angeschlossen ist
pin = 4

class DHT22_Sensor:
    @staticmethod
    # Funktion zur Temperaturmessung
    def read_temperature():
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        return temperature

    @staticmethod
    def read_humidity():
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        return humidity
    
    @staticmethod
    def get_temperature_deviation(f_temperature, temp_threshold_low, temp_threshold_high):
        to_high = f_temperature - temp_threshold_high
        to_low = f_temperature - temp_threshold_low
        if f_temperature > temp_threshold_high:
            temperature_deviation = to_high
        elif f_temperature < temp_threshold_low:
            temperature_deviation = to_low
        else:
            temperature_deviation = "   "
        return temperature_deviation
    @staticmethod
    def get_temperature_deviation_plus_minus(f_temperature, temp_threshold_low, temp_threshold_high):
        if f_temperature > temp_threshold_high:
            temp_plus_minus = '+'
        elif f_temperature < temp_threshold_low:
            temp_plus_minus = '-'
        else:
            temp_plus_minus = ' '
        return temp_plus_minus

        
