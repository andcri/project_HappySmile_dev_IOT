"""
Data Pipeline:
- collect data from the database by date
- calculate cs info
- save obtained info in new database
"""

# from database_configuration_scripts.operations_on_database_methods import get_data_values
from database_configuration_scripts.table_models import Daily_Unique_Id, Daily_Collected_Data, Calculated_Age_Gender
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, LargeBinary
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from subscriber_info import subscriber
from datetime import datetime, date
from keras.models import load_model
from imutils import paths
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import cv2
import time
import os
import face_recognition
import keras

# get values from database, the process of getting the data and put it in an array will be delegated to a method

# connection string to the database
DATABASE_URI = 'postgres://yqjmwpmnlrrehd:55176ce134225cfd8885a8dac7402fd383cae44009905d6fdda3843b80105dda@ec2-54-75-224-168.eu-west-1.compute.amazonaws.com:5432/dmbn9tt9l3mvd'
DATABASE_URI_LOCALE = 'postgres+psycopg2://pi:Mypassword@localhost:5432/devhappysmile'
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
USER = subscriber['name']


genderProto = "/home/pi/Desktop/project_HappySmile_dev/ML_Models/gender_deploy.prototxt"
genderModel = "/home/pi/Desktop/project_HappySmile_dev/ML_Models/gender_net.caffemodel"
genderNet = cv2.dnn.readNet(genderModel, genderProto)

genderList = ['Male', 'Female']

ageProto = "/home/pi/Desktop/project_HappySmile_dev/ML_Models/age_deploy.prototxt"
ageModel = "/home/pi/Desktop/project_HappySmile_dev/ML_Models/age_net.caffemodel"
ageNet = cv2.dnn.readNet(ageModel, ageProto)

ageList_detail = ['(0 - 2)', '(4 - 6)', '(8 - 12)', '(15 - 20)', '(25 - 32)', '(38 - 43)', '(48 - 53)', '(60 - 100)']
ageList = [0, 1, 2, 3, 4, 5, 6, 7]

# create engine using the uri
engine = create_engine(DATABASE_URI_LOCALE)

Session = sessionmaker(bind = engine)

s = Session()

print(engine)

today = date.today()

# query the rows of the database

rows = s.query(Daily_Collected_Data).filter(Daily_Collected_Data.date == today).all()

calculated_values = []
# iterate trough rows
for row in rows:
    image_name = row.img_name
    image_file_path = row.img_file
    times_seen = row.number_of_img
    print("----------")
    print(image_name)
    print(image_file_path)
    print(times_seen)
    print("Starting analysis")
    face = cv2.imread(image_file_path)
    blob = cv2.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
    genderNet.setInput(blob)
    genderPreds = genderNet.forward()
    gender = genderList[genderPreds[0].argmax()]
    ageNet.setInput(blob)
    agePreds = ageNet.forward()
    age = ageList[agePreds[0].argmax()]
    age_range = ageList_detail[agePreds[0].argmax()]
    print("Age Index: {}".format(age))
    print("Age Range : {}".format(age_range))
    print("Gender : {}".format(gender))
    print("----------")
    calculated_values.append([image_name, 1 if gender == 'Male' else 0, age, age_range, times_seen]) # date, string, integer, integer, string

print(calculated_values)

# write the obtained values age and gender in a row in a dedicated database

# this will be replaced by an upsert
# drop columns with the date of today if they are present
# DATABASE = 'postgres+psycopg2://postgres:myPassword@localhost:5432/postgres'

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)

s = Session()

s.query(Calculated_Age_Gender).filter(and_(Calculated_Age_Gender.date == today, Calculated_Age_Gender.subscriber == USER)).delete()

# start iteration of calculated values
for data in calculated_values:
    row = Calculated_Age_Gender(
        date=today,
        img_name=data[0],
        gender=data[1],
        age=data[2],
        age_range=data[3],
        times_seen = data[4],
        subscriber = USER
    )
    s.merge(row)
s.commit()


# add values to table in database

# commit changes

# always close a session when we finished using it
s.close()
