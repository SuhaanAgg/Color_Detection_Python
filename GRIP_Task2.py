"""
    THIS IS A COLOR DETECTOR MADE BY SUHAAN AGGARWAL FOR TSF GRIP JAN2022
    IT USES OPENCV FOR DETECTING COLOR OF A POINT IN AN IMAGE SPECIFIED BY
    THE USER.
    IT HAS TWO MODES:
        1. DBL CLICK MODE IN WHICH THE COLOR IS DETECTED AT THE POINT WHERE THE 
           USER DOUBLE CLICKS
        2. SMOOTH MODE IN WHICH THE COLOR IS DETECTED WHEREVER THE USER'S MOUSE
           POINTER IS LOCATED.
    THESE TWO MODES CAN BE TOGGLED USING "SPACEBAR"
"""

import cv2
import numpy as np
import pandas as pd
from itertools import cycle


img = cv2.imread("donut.png")

# Global Variables

tmp = 1
clicked = False
r= g= b= xpos= ypos = 0

#Reading colors.csv file with pandas
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def getColorName(R,G,B):
    """
        Takes RGB values as args and looks for an appropriate color name
        in the pandas csv data frame
    """
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

def draw_function(event, x,y,flags,param):
    """
        Function which uses x,y coordinates of mouse pointer and returns RGB values
        on triggering a certain event
    """

    if mode == 1 and event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
    
    elif mode == 0 and event == cv2.EVENT_MOUSEMOVE:
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

# Executing loop
while(1):
    
    mode = tmp%2
    cv2.imshow("image",img)
    if (clicked):
   
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        cv2.putText(img, text,(50,50),4,0.8,(255,255,255),2,cv2.LINE_8)

        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),4,0.8,(0,0,0),2,cv2.LINE_8)
            
        clicked=False

    # Change mode if user presses "spacebar"  
    if cv2.waitKey(20) & 0xFF ==32:
        tmp = tmp+1
        continue
    
    # Stop executing if user presses "esc"
    elif cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
