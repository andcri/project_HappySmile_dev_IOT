from database_configuration_scripts.config import DATABASE_URI, DATABASE_URI_LOCALE
from database_configuration_scripts.table_models import Daily_Unique_Id, Daily_Collected_Data
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, timedelta

def variables_initialization(unique_id=0, time_spent={}, day=date.today(), DATABASE=DATABASE_URI_LOCALE):
    """
    initialize the variables unique_identifier and time_spent by getting the variables values from the rispective tables.
    If todays date is not inside the table it will create a row with today date and initialize it to 0

    this method is retrieving only the unique_image_id value from the database
    the time_spent value will be retrieved after testing of the first one
    """
    # values to pass to the cam_face_recognition script
    unique_image_id_value = unique_id
    time_spent_value = time_spent

    # create engine to connect to the database
    engine = create_engine(DATABASE)

    # create a session to comunicate to the database
    Session = sessionmaker(bind=engine)

    s = Session()

    # get today date
    today = day

    # create row with initial value
    initial_value = Daily_Unique_Id(
        date = today,
        unique_image_id = 0
    )

    # try to insert the inital value if not present in the table
    try:
        s.add(initial_value)
        s.commit()
    # if the value is already inside the table we can retrieve the value form the database
    except:
        s.close()
        # initial unique_image_id value
        unique_image_id_value = s.query(Daily_Unique_Id.unique_image_id).filter(Daily_Unique_Id.date == today).first()[0]

    s.close()

    return unique_image_id_value, time_spent_value

def variables_update(unique_id, day=date.today(), DATABASE=DATABASE_URI_LOCALE):
    """
    this method will write the new values to the database
    """
    # values to update
    unique_image_id_value = unique_id

    # get today date
    today = day

    # create engine to connect to the database
    engine = create_engine(DATABASE)

    # create a session to comunicate to the database
    Session = sessionmaker(bind=engine)

    s = Session()

    # try/except to update the unique_image_id_value in the database with the new passed one
    try:
        print("updating value")
        s.query(Daily_Unique_Id).filter(Daily_Unique_Id.date == today).update({'unique_image_id': unique_image_id_value})
        s.commit()
        print("value updated")
    except:
        print("Error updating the value")


    s.close()


def write_calculated_data_to_database(array_to_database, DATABASE=DATABASE_URI_LOCALE):
    """
    method that will be used in the image_selector.py script to write the newly obtained data to the database
    """
    today = date.today()

    engine = create_engine(DATABASE)

    Session = sessionmaker(bind=engine)

    s = Session()

    s.query(Daily_Collected_Data).filter(Daily_Collected_Data.date == today).delete()
    # now that we have an instance of a session we can use it to add a row to the database
    # we create the object (row) to insert
    for array_data in array_to_database:
        # print("saving array data")
        row = Daily_Collected_Data(
            date=today,
            img_name= array_data[0],
            img_file = array_data[2],# upload the path of the image not the image file itself
            number_of_img=array_data[1],
        )

        s.merge(row)
    s.commit()
    s.close()

    def get_data_values(date):
        # get values from the day
        pass

if __name__ == "__main__":
    # first, second = variables_initialization()
    # print(first)

    # variables_update(4)
    pass
