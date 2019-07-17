from config import DATABASE_URI
from table_models import Daily_Unique_Id
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, timedelta

# create engine to connect to the database
engine = create_engine(DATABASE_URI)

# create a session to comunicate to the database
Session = sessionmaker(bind=engine)

s = Session()
print(type(s))
today = date.today()
towmorrow = date.today() + timedelta(days=1)
# create a new row to insert
row = Daily_Unique_Id(
    date = today,
    unique_image_id = 15
)
row_towmorrow = Daily_Unique_Id(
    date = towmorrow,
    unique_image_id = 1
)
print("Today: ", today)
print(type(today))
# commit the row to the table
try:
    print("inside try")
    s.add(row)
    s.commit()
    print("inserted new row")
except:
    s.close()
    # get the unique_image_id from the date
    # unique_image_id = select([Daily_Unique_Id.unique_image_id]).where(Daily_Unique_Id.date == today)
    # value = conn.execute(unique_image_id).fetchone()[0]
    value = s.query(Daily_Unique_Id.unique_image_id).filter(Daily_Unique_Id.date == today).first()[0]
    print("Day already inside, getting the value from the database and assign it to the variable")
    print("value: ", value)
# query rows inserted
print(s.query(Daily_Unique_Id.unique_image_id).filter(Daily_Unique_Id.date == today).first()[0])

s.close()