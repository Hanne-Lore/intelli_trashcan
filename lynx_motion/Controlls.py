import ssc32

ssc = ssc32.SSC32('/dev/ttyUSB0', 115200, count=1)

ssc[0].position = 2000
ssc[0].name = "Base"

ssc.commit()

while not ssc.is_done():
    print "working"
    
ssc.close();

print "done"