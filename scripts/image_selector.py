# TODO: implement a way to check the os and assign the correct path
"""
This script will analyze all the previously collected images from the cam_face_recognition script
and will determin which one are representing the same person and wich one are not.
This script will run once a day at the end of every day
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, LargeBinary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from database_configuration_scripts.operations_on_database_methods import write_calculated_data_to_database
from utility_methods import is_same_person, is_analyzable, get_image_clarity
import numpy as np
import cv2
import time
import os
import platform
import face_recognition
import shutil
from imutils import paths

start = time.time()

debug = True
imagesPath = "/home/pi/Desktop/project_HappySmile_dev_IOT/generated_folders/tmp_img_folder"
filesToUploadPath = "/home/pi/Desktop/project_HappySmile_dev_IOT/files_to_upload/"
# check on wich os we are and select the correct path to use
folder_path = imagesPath

print(folder_path)
# add check if we are on a linux or windows machine

images_name_list = os.listdir(folder_path)

# images_to_check = os.listdir(imagesPath)

print(images_name_list)

# filter only analyzable images
new_array_filtered = is_analyzable(images_name_list, folder_path)

# save the filtered images in a folder "to be uploaded"
print("saving filtered images to the folder")
for image in new_array_filtered:
    shutil.copy(imagesPath+"/"+image, filesToUploadPath)

print('new array filtered: {}'.format(new_array_filtered))
# check one by one if the images are representing the same person

print("Bucketing picture that are representing the same person")

pointer0 = 0
pointer1 = 1
same_person = []
final_array = []
if len(new_array_filtered) > 2:
    while True:
        if not new_array_filtered: # array is empty
            break
        first_person = new_array_filtered[pointer0]
        second_person = new_array_filtered[pointer1]
        if is_same_person(first_person, second_person, folder_path): # this will be substitute with the function that detect if two faces are of the same person
            print("match")
            same_person.append(second_person)
            new_array_filtered.pop(pointer1)
        else:
            print("different")
            pointer1 += 1
        if pointer1 == len(new_array_filtered):
            same_person.append(new_array_filtered[pointer0])
            new_array_filtered.pop(pointer0)
            # TODO: send the newly created same_person list to a method that will create a dictionary of key values out of them
            final_array.append(same_person)
            # reset the same_person array
            same_person = []
            # check if new_array_filtered list has more than one value inside
            if len(new_array_filtered) != 1:
                # reset the pointer1 to 1
                pointer1 = 1
            else:
                # TODO: send the one value to the dictionary builder pipeline and break out of the while loop
                same_person.append(new_array_filtered[pointer0])
                final_array.append(same_person)
                new_array_filtered.pop(pointer0)
                break
        # print(final_array)
elif len(new_array_filtered) == 1:
    # there is only one image inside the folder, we put only this one in the final array
    final_array.append([new_array_filtered[0]])
elif len(new_array_filtered) == 2:
    # there are only two images in the folder, we will compare the two images and we will add them to the final array
    if is_same_person(new_array_filtered[0], new_array_filtered[1], folder_path):
        final_array.append([new_array_filtered[0], new_array_filtered[1]])
    else:
        final_array.append([new_array_filtered[0]])
        final_array.append([new_array_filtered[1]])
print(final_array)

# check for highes clarity picture for each of the final array entry

print("Exracting highest clarity picture for each person")

send_to_database = []
for image_list in final_array:
    converted_images_list = []
    for image in image_list:
        # image contains the name of the image, not the image itsefl, we need before to create the image obj
        if platform.system() == "Linux":
            path_to_use = folder_path+"/"
            image_obj = face_recognition.load_image_file(folder_path+"/"+image)
        else:
            path_to_use = folder_path+"\\"
            image_obj = face_recognition.load_image_file(folder_path+"\\"+image)
        clarity_value = get_image_clarity(image_obj) # sudo code that will work in the non test script
        converted_images_list.append(clarity_value)
    # here we have all the converted images by blur level, we do a max to get the clearest image of the person
    value_to_keep = max(converted_images_list)
    image_index = converted_images_list.index(value_to_keep)
    image_to_send = image_list[image_index]
    # insert all the data to a new array
    send_to_database.append([image_to_send, len(image_list), path_to_use+image_to_send])

print("++")
print(send_to_database)
print("++")

# [upsert] write data to the database
write_calculated_data_to_database(send_to_database)

end = time.time()

print("total time: {}".format(end - start))

# wait one minute and start the calculate_age_gender.py

time.sleep(20)

# start calculate_age_gender.py
import calculate_age_gender
