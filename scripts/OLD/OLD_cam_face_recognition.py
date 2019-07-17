"""
once the face is recognized there is a first delay of 0.3 seconds, than the first picture is taken
after the first picture is taken we will wait for 0.5 seconds and get another one
after that the two saved images will be processed and will be detected if is the same person that is looking at the ad

WARNING

the cascade classifier is able to detect multiple faces at time, need to consider if to limit the identification to one at the time
or if we want to analyze multiple people we should program the camera in a way that it will be active to detect faces looking in its direction
every n of seconds.

to think about benefits and disadvantages of both the choiches

TODO:
- move functions in separate file
- use namespaces to contain the folders paths
- make the unique_identifier a value that we get from a database that is reinitialized to 0 every day, but if the program crushes it will
    read his latest value and uses it in the script

IMPORTANT:

Test in notebooks if the face_recognition can be done more efficently
"""
from face_recognition_methods import check_if_array_equal, add_visiting_time
from database_configuration_scripts.operations_on_database_methods import variables_initialization
import numpy as np
import cv2
import time
import os
import face_recognition

# add error control on the encoding 1 and encoding 2 for list index out of range
# if this error occures in the image2 it means that the picture was not taken properly so we do nothing and we take the next one
def same_person(historic_picture, current_picture):

    image1 = face_recognition.load_image_file(f"/home/andrea/Desktop/project_HappySmile_dev/generated_folders/tmp_img_folder/{historic_picture}")
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
# dictionary that keeps track of the times every customer spend in the shop
# this variable will be initialized reading data from the Time Spent table, if there is not a row with the current day inizialize the
# dictionary to 0
time_spent = {}
faceCascade = cv2.CascadeClassifier('../haarcascade_files/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
num = 0
previous_picture_exists = False
# this variable will get his value from the Daily Tracked Values Table, if there is not a row for the current day create one
# and initialize its value to 0
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
        print(f"unique identifier {unique_identifier}")
        # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        crop_img = img[y: y + h, x: x + w]
        # cv2.imwrite('tmp_opencv'+str(unique_identifier)+'.jpg',crop_img)
        print(type(crop_img))
        # create folder if doesnt exists
        if not os.path.exists('../generated_folders/tmp_img_folder'):
            print("folder doesn`t exists, creating a new one")
            os.makedirs('../generated_folders/tmp_img_folder')
            cv2.imwrite('../generated_folders/tmp_img_folder/opencv'+str(unique_identifier)+'.jpg',crop_img)
            # send image to the pipeline
            # TODO
        # check if a previous image exists in the folder and compare it with the new one
        previous_pictures = os.listdir("/home/andrea/Desktop/project_HappySmile_dev/generated_folders/tmp_img_folder")
        # for loop to check all images inside the folder and compare it with previously recorded ones
        """
        important:
        do not add the image in the folder for each iteration, we need before adding the image to check if all of the current images
        are not rappresenting the same person.
        TODO optional:
        Think of a way to keep track of how much time a customer is staring at the product
        """
        is_same_person = []
        for historic_picture in previous_pictures:
            print(historic_picture)
            try:
                already_inside = same_person(historic_picture, crop_img)[0]
            except:
                already_inside = True
            # check if the person in the current picture is the same as the registered one
            if not already_inside:
                # append a False to is_same_person since the person in the current picture is not the same as the one in the folder
                is_same_person.append(False)
                
                print("different person")
            else:
                # append a True to is_same_person since the person in the current picture is the same as the one in the folder
                is_same_person.append(True)
                # here i add the specific person to the time spent dictionary, the key will be the name of the person, the value
                # will be a integer that i increment every time the person is detected
                add_visiting_time(historic_picture, time_spent)
                print("same person")
                print(time_spent)
        # check if the array is_same_person has all False inside it and that
        # the first element is not True, if yes we can add the current picture to the folder
        if check_if_array_equal(is_same_person) and is_same_person[0] == False:
            # add the picture to the folder
            cv2.imwrite('../generated_folders/tmp_img_folder/opencv'+str(unique_identifier)+'.jpg',crop_img)
            print("picture added to the folder")
            # send the new person image to the pipeline i.e. add it to another specific folder
            # TODO
            print("sending picture to the pipeline")
        # else we do not add it to the folder and we continue
        unique_identifier += 1
        print(f'is the same person {is_same_person}')
        time.sleep(4)
        # add info to the database -> Update the daily Tracked Value database with the unique_identifier value (upsert)
        # add info to the database -> Update the Time Spent database with the new value (upsert)
    time.sleep(4)

    # video feed for debug pourpose
    cv2.imshow('video',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows()