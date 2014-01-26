'''
Created on Jan 20, 2014

@author: hannelore marginean
'''
import serial

class Lynx:

    # POSITIONS

    BASE_POS = 0
    FLOWER_POWER_POS = 2
    LOWER_JOINT_POS = 4
    UPPER_JOINT_POS = 6
    ZOMBIE_WRIST_POS = 8
    CLAW_POS = 10

    # min and max for every motor

    BASE_MAX = 2500  # 180 degrees
    BASE_MIN = 650  # 0 degrees

    FLOWER_POWER_MAX = 1900
    FLOWER_POWER_MIN = 650

    LOWER_JOINT_MAX = 2000
    LOWER_JOINT_MIN = 900

    UPPER_JOINT_MAX = 2400
    UPPER_JOINT_MIN = 700

    ZOMBIE_WRIST_MAX = 2380
    ZOMBIE_WRIST_MIN = 700

    CLAW_MAX = 1900
    CLAW_MIN = 1050


    def __init__(self):

        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

        if (self.ser.isOpen()):
            print "is open"
        else:
            print "is not open"
    
    def move_base(self, position_degrees):
        print "-----------------MOVING BASE----------------"
        
        if (position_degrees < 0 or position_degrees > 180):
            print "You can only move the base from 0 to 180 degrees: " + str(position_degrees) + " is not correct!"
        else:
            # this value corresponds to 180 degrees
            interval = self.BASE_MAX - self.BASE_MIN
            
            # we calculate the new position with a simple three set and add the min value of the base
            new_position = (interval * position_degrees) / 180 + self.BASE_MIN
            
            if (new_position >= self.BASE_MIN and new_position <= self.BASE_MAX):
                
                output_string = '#' + str(self.BASE_POS) + 'P' + str(new_position) + '\r'
                print "-----------start moving base: " + output_string
                self.ser.write(output_string)
                self.ser.flush()
                self.ser.close()
                print "-----------done moving BASE " + str(position_degrees) + " degrees"
            
            
            
l = Lynx()
l.move_base(-1)


