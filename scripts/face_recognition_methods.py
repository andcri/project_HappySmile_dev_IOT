import numpy as np
import cv2
import time
import os
import face_recognition

def same_person(historic_picture, current_picture):

    image1 = face_recognition.load_image_file("/home/pi/Desktop/project_HappySmile_dev/generated_folders/tmp_img_folder/{}".format(historic_picture))
    image2 = current_picture

    encoding_1 = face_recognition.face_encodings(image1)[0]

    try:
        encoding_2 = face_recognition.face_encodings(image2)[0]
    except IndexError:
        print("Image not clear, taking another one")
        return True
    
    results = face_recognition.compare_faces([encoding_1], encoding_2,tolerance=0.50)

    return results

def check_if_array_equal(iterator):
    """
    check if an array contains the same value in each position, it will stop when it
    finds a different value in the array
    """
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)

def add_visiting_time(picture_name, dict):
    """
    count the time that a user is spending inside the shop
    """
    try:
        dict[picture_name] += 1
    except:
        dict[picture_name] = 1

# add blur detection

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()