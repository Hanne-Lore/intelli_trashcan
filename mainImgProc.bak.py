import cv2
import cv2.cv as cv
import numpy as np

from opencv.ImageProcessor import *
from irobot.pyrobot import *
from math import floor


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
from lynx_motion import Controlls
lynx = Controlls.Lynx()
lynx.move_to_starting_position()

positionAverage = [[0, 0], 0]
centers = []
diameters = []
averageFramesNr = 12
currentAverageFrame = 0
frameCenter = [180, 240]
distanceThreshold = 25
firstFind = True

currentRotation = 0
currentRotationDir = 1
notDetected = 0

def getSpeedByDistance(dist):
    if dist < 1000:
        return 4
    if dist < 2000:
        return 5
    if dist < 4000:
        return 5
    return 6

def getPixelsPerRotation(diameter):
#     return (diameter * 14.83) / 62.5
    return (diameter * 8.72) / 24

def getRotThreshold(dist):
    if dist > 200:
        return 50
    elif dist > 100:
        return 40
    else:
        return 30
    
def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]

def calcCentersMedian(centers):
    x = []
    y = []
    for pos in centers:
        x.append(pos[0])
        y.append(pos[1])
    
    return [median(x), median(y)]

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
        notDetected = 0
        currentAverageFrame += 1
        centers.append([garbage[0][0] * 0.75, garbage[0][1] * 0.75])
        diameters.append(garbage[1] * 0.75)
#         centers.append([garbage[0][0], garbage[0][1]])
#         diameters.append(garbage[1])
        
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
                
            positionAverage[0] = calcCentersMedian(centers)
            positionAverage[1] = median(diameters)
            
            currentAverageFrame = 0
            direction = 'ccw' if positionAverage[0][0] < frameCenter[0] else 'cw'
            pixelsPerRotation = getPixelsPerRotation(garbage[1] * 2)
            rotVelocity = floor(abs(positionAverage[0][0] - frameCenter[0]) / pixelsPerRotation)
            print positionAverage
            
            
            cv2.circle(garbage[2], (int(positionAverage[0][0]), int(positionAverage[0][1])), 10, (0, 0, 255), 2)
            
            moved = False
            if rotVelocity < 2:
                rotVelocity = 2
                
            # Calculate the ~ distance
            area = PI * (garbage[1] ** 2)
            diameter = garbage[1] * 2
#             distance = (150 * 182) / diameter
#             distance -= 150
            distance = (125 * 210) / diameter
            distance -= 125
            
            print "Diameter: "+`diameter`
#             print 'Rotate '+`rotVelocity`
            
            centerThreshold = getRotThreshold(distance)
            if (positionAverage[0][0] < frameCenter[0] - centerThreshold or positionAverage[0][0] > frameCenter[0] + centerThreshold):
                print 'Rotate '+direction+': '+`rotVelocity`+' (ppr: '+`pixelsPerRotation`+')'
                controller.Turn(rotVelocity, direction, True)
                if direction == 'cw':
                    currentRotation += rotVelocity
                else:
                    currentRotation -= rotVelocity
                    
                moved = True
            else:
                if distance > 300:
                    distance = 300
                    
#                 print 'Raw distance: '+`distance`
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
#                 break;
            
            centers = []
            diameters = []
#             print positionAverage
    elif garbage == None:
        notDetected += 1
        
        if notDetected == 10:
            notDetected = 0
            # Nothing found, let's rotate a bit to scan the area
            if currentRotationDir == 1:
                currentRotation += 10
                rotation = 10
            else:
                currentRotation -= 10
                rotation = -10
             
            if currentRotation > 20: currentRotationDir = -1
            elif currentRotationDir < -20: currentRotationDir = 1
             
            controller.Turn(rotation, 'cw', True)
    
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


"""

"""

