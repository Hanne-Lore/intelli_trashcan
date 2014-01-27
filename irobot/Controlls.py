'''
Created on Jan 20, 2014

@author: hannelore marginean
'''
import serial
import time

class Lynx:

    BASE_NAME = 'BASE'
    FLOWER_POWER_NAME = 'FLOWER_POWER'
    LOWER_JOINT_NAME = 'LOWER_JOINT'
    UPPER_JOINT_NAME = 'UPPER_JOINT'
    ZOMBIE_WRIST_NAME = 'ZOMBIE_WRIST'
    CLAW_NAME = 'CLAW'
    
    motors = {
              # default position will be 90 degrees, aka 1500
              'BASE': 
                    {
                        'MIN': 650,
                        'MAX': 2500,
                        'SSC_POS': 0,
                        'CURRENT_POS': 0,
                        'MAX_DEGREE': 180
                    },
              'FLOWER_POWER': 
                    {
                        'MIN': 650,
                        'MAX': 1900,
                        'SSC_POS': 2,
                        'CURRENT_POS': 0,
                        'MAX_DEGREE': 125
                    },
              'LOWER_JOINT':
                    {
                        'MIN': 900,
                        'MAX': 2000,
                        'SSC_POS': 4,
                        'CURRENT_POS': 0,
                        'MAX_DEGREE': 116
                    },
              'UPPER_JOINT':
                    {
                        'MIN': 650,
                        'MAX': 2400,
                        'SSC_POS': 6,
                        'CURRENT_POS': 0,
                        'MAX_DEGREE': 180
                    },
              'ZOMBIE_WRIST':
                    {
                        'MIN': 700,
                        'MAX': 2350,
                        'SSC_POS': 8,
                        'CURRENT_POS': 0,
                        'MAX_DEGREE': 165
                    },
              'CLAW':
                    {
                        'MIN': 1100,
                        'MAX': 1800,
                        'SSC_POS': 10,
                        'CURRENT_POS': 0,
                        'MAX_DEGREE': 50
                    },
              
              }
    def __init__(self):

        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

        if (self.ser.isOpen()):
            print "is open"
        else:
            print "is not open"
            
    def move_general(self, position_degrees, motor_name):
        
        motor_data = self.motors.get(motor_name)
        if (position_degrees < 0 or position_degrees > motor_data.get('MAX_DEGREE') ):
            print "You can only move the "+ motor_name +" from 0 to " + str(motor_data.get('MAX_DEGREE')) +" degrees/mm: " + str(position_degrees) + " is not correct!"
        else:
            interval = motor_data.get('MAX')- motor_data.get('MIN')
            
            # we calculate the new position with a simple three set and add the min value of the base
            new_position = (interval * position_degrees) / motor_data.get('MAX_DEGREE') + motor_data.get('MIN')
            
            if (new_position >= motor_data.get('MIN') and new_position <= motor_data.get('MAX')):
                
                output_string = '#' + str(motor_data.get('SSC_POS')) + 'P' + str(new_position) + '\r'
                print "-----------start moving "+ motor_name +": " + output_string
                self.ser.write(output_string)
                self.ser.flush()
                #self.ser.close()
                print "-----------done moving BASE " + str(position_degrees) + " degrees"
    
    def move_to_starting_position(self):
        self.move_general(90, self.BASE_NAME)
        time.sleep(0.5)
        self.move_general(90, self.FLOWER_POWER_NAME)
        time.sleep(0.5)
        self.move_general(0, self.LOWER_JOINT_NAME)
        time.sleep(0.5)
        self.move_general(90, self.UPPER_JOINT_NAME)
        time.sleep(0.5)
        self.move_general(90, self.ZOMBIE_WRIST_NAME)
        time.sleep(0.5)
        self.move_general(0, self.CLAW_NAME)
        
        
        
l = Lynx()
l.move_to_starting_position()




