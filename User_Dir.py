__author__ = 'cwong_000'

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    screenname = Column(String(250), nullable=False)
    password = Column(String(25), nullable=False)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Query to check if a User exist in the database
def check_if_user_exist(username):
    query_person = session.query(User).filter(User.username == username)

    if (query_person != None):
        return {'valid': False, 'message' : 'User not exist in database'}
    else:
        return {'valid': True, 'message' : 'User exists in database'}

# Insert a User in the user table
def add_user_to_database(new_username, new_screenname, new_password):
    new_user = User(username=new_username, screenname = new_screenname, password = new_password)
    session.add(new_user)
    session.commit()

# Query to check if a User with the username and password provided matches any entry within the database
def check_if_user_can_login(username, password):
    query_person = session.query(User).filter(User.username == username, User.password == password)

    if (query_person != None):
        return {'valid': False, 'message' : 'Username or password incorrect'}
    else:
        return {'valid': True, 'message' : 'Log in success!'}