# models.py contains all of the declarative models for our database.
#
# docs => https://docs.sqlalchemy.org/en/13/orm/tutorial.html


import sqlalchemy
import sqlalchemy.ext.declarative as sqlalchemy_declarative
from sqlalchemy import Column, Integer, String

# docs => https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping
Base = sqlalchemy_declarative.declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}')>"

    @property
    def data(self):
        return {
            "id": self.id,
            "name": self.name,
        }
