import cv2
import cv2.cv as cv
import numpy as np

from opencv.ImageProcessor import *
from irobot.pyrobot import *
from math import floor
from lynx_motion import Controlls


PROP_SATURATION = 12
PI = 3.14159265

# Display window
cv2.namedWindow("original")

# Initiate webcam
webcam = cv2.VideoCapture(0)
# webcam.set(3, 800)
# webcam.set(4, 600)

# Initiate the graphics processor
ImgProc = ImageProcessor()    

# iRobot controller
controller = iRobotController()

#Lynx arm controller
lynx = Controlls.Lynx()
lynx.move_to_starting_position()

positionAverage = [[0, 0], 0]
averageFramesNr = 12
currentAverageFrame = 0
frameCenter = [180, 240]
distanceThreshold = 25
firstFind = True

def getSpeedByDistance(dist):
    if dist < 1000:
        return 4
    if dist < 2000:
        return 5
    if dist < 4000:
        return 5
    return 6

def getPixelsPerRotation(diameter):
    return (diameter * 14.83) / 62.5

def getRotThreshold(dist):
    if dist > 200:
        return 50
    elif dist > 100:
        return 40
    else:
        return 30

while True:
    # Get a frame
    webcamRunning, frame = webcam.read()
    if not webcamRunning:
        continue;
    
    # Resize the frame
    frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
    
    # Search for garbage in the frame
    garbage = ImgProc.detectGarbage(frame)
    if garbage != None and currentAverageFrame < averageFramesNr:
        currentAverageFrame += 1
        positionAverage[0][0] += garbage[0][0] * 0.75
        positionAverage[0][1] += garbage[0][1] * 0.75
        positionAverage[1] += garbage[1] * 0.75
    elif currentAverageFrame == averageFramesNr and garbage != None:
        if firstFind:
            firstFind = False
        else:
            positionAverage[0][0] /= averageFramesNr
            positionAverage[0][1] /= averageFramesNr
            positionAverage[1] /= averageFramesNr
            currentAverageFrame = 0
            direction = 'ccw' if positionAverage[0][0] < frameCenter[0] else 'cw'
            pixelsPerRotation = getPixelsPerRotation(garbage[1] * 2)
            rotVelocity = floor(abs(positionAverage[0][0] - frameCenter[0]) / pixelsPerRotation)
            print positionAverage
            
            
            cv2.circle(garbage[2], (int(positionAverage[0][0]), int(positionAverage[0][1])), 10, (0, 0, 255), 2)
            
            moved = False
            print 'veloc = '+`rotVelocity`
            if rotVelocity < 2:
                rotVelocity = 2
                
            # Calculate the ~ distance
            area = PI * (garbage[1] ** 2)
            diameter = garbage[1] * 2
#             distance = (150 * 182) / diameter
#             distance -= 150
            distance = (125 * 228) / diameter
            distance -= 125
            
            print "Diameter: "+`diameter`
            
            centerThreshold = getRotThreshold(distance)
            if (positionAverage[0][0] < frameCenter[0] - centerThreshold or positionAverage[0][0] > frameCenter[0] + centerThreshold):
                print 'Rotate '+direction+': '+`rotVelocity`+' (ppr: '+`pixelsPerRotation`+')'
                controller.Turn(rotVelocity, direction, True)
                moved = True
            else:
                if distance > 300:
                    distance = 300
                    
                print 'Raw distance: '+`distance`
                if distance < distanceThreshold and distance > -distanceThreshold:
                    distance = 0
            
                if distance != 0:
                    moved = True
                    print 'Move forward '+`distance`+'mm'
                    controller.MoveForward(distance, getSpeedByDistance(distance), True)
            
            if not moved:
                lynx.move_down()
                lynx.close_claw()
                lynx.move_up()
                lynx.open_claw()
                time.sleep(1)
                lynx.move_starting_positions_smoothly()
                break;
                
            print positionAverage
    
    frame = cv2.medianBlur(frame, 11)
    
    # controller.MoveForward(500, 5, True)
    
    # Display the frame
    if garbage != None:
        cv2.imshow("original", garbage[2])
    else:
        cv2.imshow("original", frame)
    
    # Exit on ESC
    key = cv2.waitKey(20)
    if key in [27, ord('Q'), ord('q')]:
        break
    

