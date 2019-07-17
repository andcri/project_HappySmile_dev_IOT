from config import DATABASE_URI, DATABASE_URI_LOCALE
from table_models import Base
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URI)

Base.metadata.drop_all(engine)

# create all the tables defined as classes that inherit from Base
Base.metadata.create_all(engine)
