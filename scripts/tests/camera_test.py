import numpy as np
import cv2
import time

faceCascade = cv2.CascadeClassifier('../../haarcascade_files/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
num = 0
look = True
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,  
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        print("found")
        print(f"faces: {faces}")
        time.sleep(0.3)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        crop_img = img[y: y + h, x: x + w]
        # cv2.imwrite('../Test_generated_files/opencv_croppedNormal'+str(num)+'.jpg',crop_img)
        time.sleep(0.1)
        num += 1
        
    


    cv2.imshow('video',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
    # add a here a time.sleep to execute the loop every n seconds
cap.release()
cv2.destroyAllWindows()
