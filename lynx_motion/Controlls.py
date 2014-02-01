'''
Created on Jan 20, 2014

@author: hannelore marginean
'''
import serial
import pprint
import datetime
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
                self.motors[motor_name]['CURRENT_POS'] = new_position
                print "-----------done moving BASE " + str(position_degrees) + " degrees"
                
                
    def move_general_real(self, new_position, motor_name):
        
        motor_data = self.motors.get(motor_name)
        if (new_position >= motor_data.get('MIN') and new_position <= motor_data.get('MAX')): 
                output_string = '#' + str(motor_data.get('SSC_POS')) + 'P' + str(new_position) + '\r'
                print "-----------start moving "+ motor_name +": " + output_string
                self.ser.write(output_string)
                self.motors[motor_name]['CURRENT_POS'] = new_position
        else:
            print "You can only move the "+ motor_name +" from " + motor_data.get('MIN') + " to " + str(motor_data.get('MAX')) +": " + str(new_position) + " is not correct!"
    
    def move_to_starting_position(self):
        self.move_general(90, self.BASE_NAME)
        self.move_general(90, self.FLOWER_POWER_NAME)
        self.move_general(0, self.LOWER_JOINT_NAME)
        self.move_general(90, self.UPPER_JOINT_NAME)
        self.move_general(90, self.ZOMBIE_WRIST_NAME)
        self.move_general(0, self.CLAW_NAME)
        
        pprint.PrettyPrinter().pprint(self.motors)
        
    def get_smooth_position(self, duration, starting_position, ending_position, current_time):
        
        print "Duration:" + str(duration) + " Start pos: " + str(starting_position) + "    End pos: " + str(ending_position) + " Current time: " + str(current_time)
        print "Ret position: " + str(starting_position + (ending_position - starting_position) * current_time / duration)
        return starting_position + (ending_position - starting_position) * current_time / duration
        
            
    def move_smoothly(self, motors_position, time_interval):
        print "\n-------------- MOVE SMOOTHLY -----------------\n"
        starting_time = time.time() * 1000
        ending_time = starting_time + time_interval
        
        current_time = time.time() * 1000
        
        for motor_name, final_pos in motors_positions.iteritems():
            interval = self.motors[motor_name].get('MAX')- self.motors[motor_name].get('MIN')
            new_position = (interval * final_pos) / self.motors[motor_name].get('MAX_DEGREE') + self.motors[motor_name].get('MIN')
            motors_positions[motor_name]= new_position
        
        while( current_time < ending_time ):
            delta_time = current_time - starting_time
            
            print "Iteration\n"
            
            for motor_name, final_pos in motors_positions.items():
                print motor_name + "\n\n"
                new_position = self.get_smooth_position(time_interval, self.motors[motor_name]['CURRENT_POS'], final_pos, delta_time)
                #print motor_name + " position: " + str(new_position)
                self.move_general_real(new_position, motor_name)
            
            time.sleep(0.001)
            current_time = time.time() * 1000
        
        print "Smooth motion done\n"
        
        for motor_name, final_pos in motors_positions.items():
            self.move_general_real(final_pos, motor_name)
            self.motors[motor_name]['CURRENT_POS'] = final_pos
            
        #pprint.PrettyPrinter().pprint(self.motors)
        
                
l = Lynx()
l.move_to_starting_position()
time.sleep(1);
#l.move_general_smoothly(50, l.CLAW_NAME)
motors_positions = {
                        l.BASE_NAME: 120,
                        l.FLOWER_POWER_NAME: 60,
                        l.LOWER_JOINT_NAME: 30,
                        l.UPPER_JOINT_NAME: 40,
                        l.ZOMBIE_WRIST_NAME: 45,
                        l.CLAW_NAME: 30
                    
                    }
#l.move_smoothly(motors_positions, 10000)





