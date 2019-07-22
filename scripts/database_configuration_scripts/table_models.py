# contains the models of the tables that we use in our database

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, JSON

Base = declarative_base()

class Daily_Unique_Id(Base):
    __tablename__ = 'Daily_Unique_Id'
    date = Column(Date, primary_key=True)
    unique_image_id = Column(Integer)
    
    def __repr__(self):
        return "<Daily_Unique_Id(date='{}', unique_image_id='{}')>"\
                .format(self.date, self.unique_image_id)

class Daily_Collected_Data(Base):
    __tablename__ = 'Daily_Collected_Data'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    img_name = Column(String)
    img_file = Column(String)
    number_of_img = Column(Integer)
    
    def __repr__(self):
        return "<Daily_Collected_Data(id='{}', date='{}', img_name='{}', number_of_img='{}')>"\
                .format(self.id, self.date, self.img_name, self.img_file, self.number_of_img)

class Calculated_Age_Gender(Base):
    __tablename__ = 'Calculated_Age_Gender'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    img_name = Column(String)
    gender = Column(Integer)
    age = Column(Integer)
    age_range = Column(String)
    times_seen = Column(Integer)
    subscriber = Column(String)
    
    def __repr__(self):
        return "<Calculated_Age_Gender(id='{}', date='{}', img_name='{}', number_of_img='{}')>"\
                .format(self.id, self.date, self.img_name, self.gender, self.age, self.age_range)

class Logs(Base):
    __tablename__ = 'Logs'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    subscriber = Column(String)
    text = Column(String)
    added_info = Column(JSON)

    
    def __repr__(self):
        return "<Daily_Unique_Id(date='{}', unique_image_id='{}')>"\
                .format(self.date, self.subscriber)