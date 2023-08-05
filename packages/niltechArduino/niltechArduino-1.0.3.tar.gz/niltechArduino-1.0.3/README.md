##example code

##to get port value
from niltechArduino import Arduino
x = Arduino.getPort()
## x now contains name of arduino port
ser = serial.Serial(x, 9600, timeout=2)
input = ser.readline()

print(input.decode("utf-8"))


#################################################
##To read incoming data, The code will do everything
x = Arduino.readData('x','y',9600,2)
#First argument(string) is start byte
#second argument(string) is stop byte
#Third argument(integer) is Baud Rate
#Last is TimeOut(integer) in seconds

print x

###############################################
#To extract data after reading

from niltechArduino import Arduino

import serial

import time

x = arduinoPort.read()

ser = serial.Serial(x, 9600, timeout=2)


while 1:





        input = ser.readline()

        print Arduino.extractData(input)

        print("-----------------------")



        time.sleep(1)
