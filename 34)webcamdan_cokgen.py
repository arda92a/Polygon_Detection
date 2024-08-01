import cv2
import numpy as np

def nothing(x):
    pass

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Create a window for the trackbars
cv2.namedWindow("Settings")

# Create trackbars for color change
cv2.createTrackbar("Lower-Hue","Settings",0,180,nothing)
cv2.createTrackbar("Lower-Saturation","Settings",0,255,nothing)
cv2.createTrackbar("Lower-Value","Settings",0,255,nothing)
cv2.createTrackbar("Upper-Hue","Settings",0,180,nothing)
cv2.createTrackbar("Upper-Saturation","Settings",0,255,nothing)
cv2.createTrackbar("Upper-Value","Settings",0,255,nothing)

font = cv2.FONT_HERSHEY_SIMPLEX

while 1:

    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    lower_h = cv2.getTrackbarPos("Lower-Hue","Settings")
    lower_s = cv2.getTrackbarPos("Lower-Saturation","Settings")
    lower_v = cv2.getTrackbarPos("Lower-Value","Settings")
    upper_h = cv2.getTrackbarPos("Upper-Hue","Settings")
    upper_s = cv2.getTrackbarPos("Upper-Saturation","Settings")
    upper_v = cv2.getTrackbarPos("Upper-Value","Settings")

    # Define the lower and upper bounds for the HSV values
    lower_color = np.array([lower_h,lower_s,lower_v])
    upper_color = np.array([upper_h,upper_s,upper_v])

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # Create a mask with the specified bounds
    mask = cv2.inRange(hsv,lower_color,upper_color)

    # Perform erosion to remove noise
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask,kernel)

    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # Calculate the area of each contour
        area = cv2.contourArea(cnt)

        # Approximate the shape of the contour
        epsilon = 0.02*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        # If the contour area is significant, identify the shape
        if area > 400:
            cv2.drawContours(frame,[approx],0,(0,0,0),5)
            if len(approx) == 3:
                cv2.putText(frame,"Triangle",(x,y),font,1,(0,0,0))
            elif len(approx) == 4:
                cv2.putText(frame,"Rectangle",(x,y),font,1,(0,0,0))
            elif len(approx) == 5:
                cv2.putText(frame,"Pentagon",(x,y),font,1,(0,0,0))
            elif len(approx) == 6:
                cv2.putText(frame,"Hexagon",(x,y),font,1,(0,0,0))
            elif len(approx) > 6:
                cv2.putText(frame,"Triangle",(x,y),font,1,(0,0,0))
                
    cv2.imshow("Frame",frame)
    cv2.imshow("Mask",mask)

    if cv2.waitKey(3) & 0xFF == ord("q") :
        break

cap.release()
cv2.destroyAllWindows()