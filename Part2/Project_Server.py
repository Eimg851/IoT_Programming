import bluetooth
from r7insight import R7InsightHandler
import logging
import Adafruit_DHT
import datetime

#Connect to InsightOps to log data
log = logging.getLogger('r7insight')
log.setLevel(logging.INFO)
test = R7InsightHandler('76f50ffb-f011-4ce3-bce6-542fb9474fdc', 'eu')
log.addHandler(test)

#Listen as master device for slaves waiting to connect
server_sock=bluetooth.BluetoothSocket( bluetooth.L2CAP )
port = 0x1001

server_sock.bind(("",port))
server_sock.listen(1)

try:
    client_sock,address = server_sock.accept()
    print("Accepted connection from ",address)
    
    #Listen and receive data to log to file
    while True:
        data = client_sock.recv(1024)
        log.info(str(data))
        humidity, temperature = Adafruit_DHT.read_retry(sensor=11, pin=4)
        timestamp = datetime.datetime.now()
        log.info("{} \tSensorID=Eimear, Temperature={}, Humidity={}".format(timestamp, temperature, int(humidity)))
    client_sock.close()
    server_sock.close()
except:
    print("Connection failed. Please try again.")
    server_sock.close()