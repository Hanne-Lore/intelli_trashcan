import cv2
import cv2.cv as cv
import numpy as np

class ImageProcessor:
    
    def __init__(self):
        # Define PI (used in calculating circle area)
        self.PI = 3.14159265
        
        # Compute the circle's contour
        self.circleImg = cv2.imread("opencv/circle.jpg", 0)
        self.circleContours, nothing = cv2.findContours(self.circleImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.circleContour = self.circleContours[0]
            
    
    """
    Detect garbage
    @return [center, radius, frame] of a garbage if detected
            None otherwise
    """
    def detectGarbage(self, frame):
        # Convert to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.medianBlur(hsv, 11)
        
        # Create masks for blue, red and yellow
        masks = []
        masks.append(cv2.inRange(hsv, np.array([80, 50, 0]), np.array([100, 255, 255]))) # Blue mask
        masks.append(cv2.inRange(hsv, np.array([0, 130, 40]), np.array([10, 255, 255]))) # Red mask
        masks.append(cv2.inRange(hsv, np.array([20, 130, 40]), np.array([30, 255, 255]))) # Yellow mask
        
        # Find the contours
        contours = [None, None, None]
        contours[0], nothing = cv2.findContours(masks[0], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours[1], nothing = cv2.findContours(masks[1], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours[2], nothing = cv2.findContours(masks[2], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Check the contours for each color
        for i in range(0, 3):
            if i != 1: continue
            contour = contours[i]
            
            # Get the largest contour and check for some requirments (area, similarity with a circle)
            if contour != None and len(contour) > 0:
                cnt = -1 # The contours index
                maxArea = 0 # The max area
                for j in range(0, len(contour)):
                    # Check the similarity with a circle
                    circleSimilarity = cv2.matchShapes(contour[j], self.circleContour, cv2.cv.CV_CONTOURS_MATCH_I1, 0)
                    if circleSimilarity > 1: continue;
                    print circleSimilarity
                    
                    # Get the area of the contour
                    newArea = cv2.contourArea(contour[j])
                    
                    # If it's too small, don't take it in consideration
                    if newArea < 300: continue
                    
                    # If it's the largest, set it as the found contour
                    if newArea > maxArea:
                        cnt = j
                        maxArea = newArea
                
                # If no contour matching the conditions was found, continue
                if cnt == -1: continue
                
                # Get the minimum enclosing circle for the contour
                (x, y), radius = cv2.minEnclosingCircle(contour[cnt])
                center = (int(x), int(y))
                radius = int (radius)
                
                # Draw the circle
                cv2.circle(frame, center, radius, (0, 255, 0), 2)
#                 cv2.drawContours(frame, contour[cnt], -1, (0, 255, 0))
                
                # Garbage detected
                return [center, radius, frame]
            
        return None