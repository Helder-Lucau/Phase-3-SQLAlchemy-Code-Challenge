from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

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
    
    # Creating a relationship
    customer = association_proxy('reviews', 'customer_rv', 
        creator=lambda cs: Review(customer=cs))
    reviews = relationship('Review', back_populates='restaurant_rv')
    
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"firstName{self.first_name}, " \
            + f"lastName {self.last_name}"  
    
    # Create relationship 
    review = relationship('Review', back_populates='review')
    restaurant = association_proxy('review', 'restaurant_rv',
            creator=lambda rs: Review(restaurant=rs))

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    star_rating = Column(Integer())
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"firstName{self.star_rating}, " \
            + f"lastName {self.last_name}"  
    
    # create relationship
    restaurant_rv = relationship('Restaurant', back_populates='reviews')
    customer_rv = relationship('Customer', back_populates='reviews')