# # contains the models of the tables that we use in our database

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, LargeBinary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import numpy as np
import cv2
import time
import os
import face_recognition
from imutils import paths

Base = declarative_base()

class Daily_Collected_Data(Base):
    __tablename__ = 'Daily_Collected_Data'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    img_name = Column(String)
    img_file = Column(String)
    number_of_img = Column(Integer)
    
    def __repr__(self):
        return "<Daily_Collected_Data(id='{}', date='{}', img_name='{}', number_of_img='{}')>"\
                .format(self.id, self.date, self.img_name, self.number_of_img)

# connection string to the database
DATABASE_URI = 'postgres://yqjmwpmnlrrehd:55176ce134225cfd8885a8dac7402fd383cae44009905d6fdda3843b80105dda@ec2-54-75-224-168.eu-west-1.compute.amazonaws.com:5432/dmbn9tt9l3mvd'

# image path
windowsImagePath = "C:\\Users\\Andrea\\Desktop\\project_HappySmile_dev\\generated_folders\\tmp_img_folder\\andrea_2.jpg"

# create engine using the uri
engine = create_engine(DATABASE_URI)

# create all the tables defined as classes that inherit from Base
# Base.metadata.create_all(engine)

# Using a session to make transactions

Session = sessionmaker(bind = engine)

s = Session()

today = date.today()

# now that we have an instance of a session we can use it to add a row to the database
# we create the object (row) to insert
row = Daily_Collected_Data(
    date=today,
    img_name='opencv1.jpg',
    img_file = windowsImagePath,# upload the path of the image not the image file itself
    number_of_img=700,
)

s.add(row)
s.commit()

# querying rows

# print(s.query(Book).first())

# for more filtering and querying options check
# https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/
 
# always close a session when we finished using it
s.close()