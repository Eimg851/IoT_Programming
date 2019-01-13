import Adafruit_DHT
import datetime

temperatureAlertDictionary = {
                xrange(0, 6) : "It is very cold",
		xrange(6,11) : "It is cold",
		xrange(22,100) : "It is very hot"
                }

humidityAlertDictionary = {
		xrange(0,31): "Humidity is low",
		xrange(80,101): "Humiditiy is very high"
		}

while True:
	f = open("DHTLogsAssignment1.txt", "a")
	alerts=[]
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
	humidity, temperature = Adafruit_DHT.read_retry(sensor=11 ,pin=4, delay_seconds=4)
	f.write("\n"+timestamp+"\tTemperature={}, Humidity={}% ".format(int(temperature), int(humidity)))
	if humidity in range(31,81) and temperature in range(11,22):
		continue
	else:
		for key in humidityAlertDictionary:
    			if humidity in key:
        			alerts.append(humidityAlertDictionary[key])
        			break

		for key in temperatureAlertDictionary:
         	      	if temperature in key:
        	               	alerts.append(temperatureAlertDictionary[key])
                        	break
		f.write("\n"+timestamp+"\t"+" ".join(alerts))
	f.close()
