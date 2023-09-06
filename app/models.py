from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy

engine = create_engine('sqlite:///restaurant.db')

Base = declarative_base()
session = sessionmaker(bind=engine)
session = session()


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), index=True)
    price = Column(Integer())

    def __repr__(self):
        return f"Restaurant {self.id}: " \
            + f"{self.name}, " \
            + f"Price {self.price}"

    # Creating a relationship
    customer = association_proxy(
        'reviews', 'customer_rv', creator=lambda cs: Review(customer=cs))
    reviews = relationship('Review', back_populates='restaurant_rv')

    # return a collection of all the reviews for the Restaurant
    def restaurant_customers(self):
        return [review for review in session.query(Review).filter.restaurant_id == self.id]

    # returns a collection of all the customers who reviewed the Restaurant
    def customers_reviews(self):
        return self.customers


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"firstName{self.first_name}, " \
            + f"lastName {self.last_name}"

    # creating relationship
    reviews = relationship('Review', back_populates='customer_rv')
    restaurant = association_proxy(
        'reviews', 'restaurant_rv', creator=lambda rs: Review(restaurant=rs))

    # return a collection of all the reviews that customer has left
    def customer_reviews(self):
        return [reviews for reviews in session.query(Review).filter(Review.id == self.id)]

    # return a collection of all the restaurants that the customer has reviewed
    def customer_reviewed(self):
        return self.restaurants

    # return the full name of the customer
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    # creates a new review for the restaurant with the given restaurant id
    def add_review(self, restaurant, rating):
        review = Review(Customer_id=self.id, restaurant_id=restaurant.id, rating=rating)
        session.add(review)
        session.commit()

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

    # should return a collection of all the reviews that the customer has left
    def review_customer(self):
        return session.query(Customer).filter(Customer.id == self.customer_id).first()

    # return the restaurant instance for this review
    def review_restaurant(self):
        return session.query(Customer).filter(Customer.id == self.customer_id).first()
