import cv2
import cv2.cv as cv
import numpy as np

from opencv.ImageProcessor import *

# Display window
cv2.namedWindow("original")

# Initiate webcam
webcam = cv2.VideoCapture(1)
if webcam.isOpened(): # try to get the first frame
    webcamRunning, frame = webcam.read()
else:
    webcamRunning = False

# Initiate the graphics processor
ImgProc = ImageProcessor()    

while webcamRunning:
    # Get a frame
    webcamRunning, frame = webcam.read()
    
    # Resize the frame
    frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
    
    # Search for garbage in the frame
    garbage = ImgProc.detectGarbage(frame)
    
    # Display the frame
    if garbage != None:
        cv2.imshow("original", garbage[2])
    else:
        cv2.imshow("original", frame)
    
    # Exit on ESC
    key = cv2.waitKey(20)
    if key in [27, ord('Q'), ord('q')]:
        break