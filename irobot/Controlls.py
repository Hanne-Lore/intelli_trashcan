'''
Created on Jan 20, 2014

@author: hannelore marginean
'''

import serial
ser = serial.Serial(port = '/dev/ttyUSB1', 
                    baudrate = 9600, 
                    parity=serial.PARITY_ODD,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.SEVENBITS)

ser.open()
if ( ser.isOpen() ):
    print "is open"
else:
    print "is not open";
    
