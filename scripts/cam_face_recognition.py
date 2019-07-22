"""
This script will use a cam(pc webcam, external cam) to recognize when a face is in front of it and take a picture of it.
After the picture is taken will be checked the level of quality of the picture, if good enough it will be saved and utilized later in
another script

TODO:
- move functions in separate file
- use namespaces to contain the folders paths
"""
from face_recognition_methods import check_if_array_equal, add_visiting_time, variance_of_laplacian
from database_configuration_scripts.operations_on_database_methods import variables_initialization, variables_update
from subscriber_info import subscriber
import datetime
import numpy as np
import cv2
import time
import os
import face_recognition

# add error control on the encoding 1 and encoding 2 for list index out of range
# if this error occures in the image2 it means that the picture was not taken properly so we do nothing and we take the next one
def same_person(historic_picture, current_picture):

    image1 = face_recognition.load_image_file("/home/pi/Desktop/project_HappySmile_dev_IOT/generated_folders/tmp_img_folder/{}".format(historic_picture))
    image2 = current_picture

    try:
        encoding_1 = face_recognition.face_encodings(image1)[0]
        encoding_2 = face_recognition.face_encodings(image2)[0]
    except IndexError:
        print("Image not clear, taking another one")
        # optional: add logic to do not execute the following code after this one
        return True
    
    results = face_recognition.compare_faces([encoding_1], encoding_2,tolerance=0.50)

    return results

# add check regarding the time that the script is run, if the script is run before the subscriber end_daytime value the script will run
# else the script will not run

current_time = datetime.datetime.now().time()

if current_time > subscriber['start_day_time'] and current_time < subscriber['end_day_time']:


    faceCascade = cv2.CascadeClassifier('/home/pi/Desktop/project_HappySmile_dev_IOT/haarcascade_files/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    num = 0
    previous_picture_exists = False
    # this variable will get his value from the Daily Tracked Values Table
    unique_identifier, time_spent = variables_initialization()
    while num < 1:
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
            time.sleep(0.35)
            print("found")
            print("unique identifier {}".format(unique_identifier))
            # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            crop_img = img[y: y + h, x: x + w]
            # cv2.imwrite('tmp_opencv'+str(unique_identifier)+'.jpg',crop_img)
            print(type(crop_img))
            # check if image is blurred
            is_not_blured = variance_of_laplacian(crop_img) >= 110
            # create folder if doesnt exists
            if not os.path.exists('/home/pi/Desktop/project_HappySmile_dev_IOT/generated_folders/tmp_img_folder'):
                print("folder doesn`t exists, creating a new one")
                os.makedirs('/home/pi/Desktop/project_HappySmile_dev_IOT/generated_folders/tmp_img_folder')
            # check if the image is not blurred
            # if not blurred save it to the folder
            if is_not_blured:
                print("good enought i save it ")
                cv2.imwrite('/home/pi/Desktop/project_HappySmile_dev_IOT/generated_folders/tmp_img_folder/happysmile'+str(unique_identifier)+'.jpg',crop_img)
                time.sleep(2)
            else:
                print("not good enough taking the next one")
                time.sleep(2)
            unique_identifier += 1
            # add info to the database -> Update the daily Tracked Value database with the unique_identifier value (upsert)
            variables_update(unique_identifier)
        # video feed for debug pourpose
        # cv2.imshow('video',img)
        # k = cv2.waitKey(30) & 0xff
        # if k == 27: # press 'ESC' to quit
        #     break
    cap.release()
    cv2.destroyAllWindows()
    
else:
    print("it s not the time to work, sleep mode activated :)")
