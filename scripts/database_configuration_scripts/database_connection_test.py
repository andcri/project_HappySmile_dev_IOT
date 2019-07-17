from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


# define the Table schema as a class
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    published = Column(Date)
    
    def __repr__(self):
        return "<Book(title='{}', author='{}', pages={}, published={})>"\
                .format(self.title, self.author, self.pages, self.published)

# connection string to the database
DATABASE_URI = 'postgres://yqjmwpmnlrrehd:55176ce134225cfd8885a8dac7402fd383cae44009905d6fdda3843b80105dda@ec2-54-75-224-168.eu-west-1.compute.amazonaws.com:5432/dmbn9tt9l3mvd'

# create engine using the uri
engine = create_engine(DATABASE_URI)

# Base.metadata.drop_all(engine)

# create all the tables defined as classes that inherit from Base
# Base.metadata.create_all(engine)

# Using a session to make transactions

Session = sessionmaker(bind = engine)

s = Session()

# now that we have an instance of a session we can use it to add a row to the database
# we create the object (row) to insert
book = Book(
    title='Deep Learning',
    author='Ian Goodfellow',
    pages=775,
    published=datetime(2016, 11, 18)
)

s.add(book)
s.commit()

# querying rows

print(s.query(Book).first())

# for more filtering and querying options check
# https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/
 
# always close a session when we finished using it
s.close()