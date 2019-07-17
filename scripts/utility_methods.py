
import numpy as np
import cv2
import time
import os
import platform
import face_recognition
from imutils import paths

# method to check if two images are of the same person, this will be moved on a separate file
def is_same_person(image1, image2, path):
    if platform.system() == "Linux":
        first_image = face_recognition.load_image_file(path+"/"+image1)
        second_image = face_recognition.load_image_file(path+"/"+image2)
    else:
        first_image = face_recognition.load_image_file(path+"\\"+image1)
        second_image = face_recognition.load_image_file(path+"\\"+image2)
    print(image2)
    
    encoding1 = face_recognition.face_encodings(first_image)[0]
    encoding2 = face_recognition.face_encodings(second_image)[0]

    results = face_recognition.compare_faces([encoding1], encoding2, tolerance=0.60)

    return results[0]

def is_analyzable(array, path):
    final_array = []
    for index, single_image in enumerate(array):
        # print(f"analyzing {single_image}")
        image_to_analyze = face_recognition.load_image_file(path+"/"+single_image)
        try:
            encoding = face_recognition.face_encodings(image_to_analyze)[0]
            # print("image is valid")
            final_array.append(single_image)
        except:
            # print(f'image {single_image} not valid')
            pass
    return final_array


# method to check the clarity of an image
def get_image_clarity(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()