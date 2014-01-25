'''
Created on Jan 20, 2014

@author: hannelore marginean
'''

import serial
ser = serial.Serial(port = '/dev/ttyUSB0', 
                    baudrate = 115200)

#ser.open()

if ( ser.isOpen() ):
    print "is open"
else:
    print "is not open"

ser.write('#0P1100' + '\r')
ser.write(bytes([0]))
ser.flush()

ser.close()

print "done"
