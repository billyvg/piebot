"""Handles database connection, and all that fun stuff.
@package ppbot

"""

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

engine = create_engine('postgres://ppbot@localhost/ppbot')

metadata = MetaData()

users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('password', String),
    Column('access', Integer)
)


metadata.create_all(engine)