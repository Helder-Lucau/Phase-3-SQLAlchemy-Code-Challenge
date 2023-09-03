from sqlalchemy import create_engine
from sqlalchemy import (Column, Integer, String)

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///restaurant.db')

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'
  
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Price {self.price}"
    
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"firstName{self.first_name}, " \
            + f"lastName {self.last_name}"   
    
# class Review(Base):
#     pass
