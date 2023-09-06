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
    customer = association_proxy('reviews', 'customer_rv', creator=lambda cs: Review(customer=cs))
    reviews = relationship('Review', back_populates='restaurant_rv')

    # return a collection of all the reviews for the Restaurant
    def restaurant_reviews(self):
        return [review for review in session.query(Review).filter.restaurant_id == self.id]
    
    # returns a collection of all the customers who reviewed the Restaurant
    def restaurant_customers(self):
        return self.customer
    
    # returns one restaurant instance for the restaurant that has the highest price
    def fanciest(self):
        return session.query(Restaurant).order_by(self.price.desc()).first()

    # returns a list of strings with all the reviews for this restaurant 
    # def  all_reviews(self):
    #     return [f'Review for {self.name} by {self.customer.full_name()}: {review.star_rating} stars.' for review in self.reviews]
    
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    def __repr__(self):
        return f"Customer={self.id}: " \
            + f"first_name={self.first_name}, " \
            + f"last_name={self.last_name}"

    # creating relationship
    reviews = relationship('Review', back_populates='customer_rv')
    restaurant = association_proxy('reviews', 'restaurant_rv', creator=lambda rs: Review(restaurant=rs))

    # return a collection of all the reviews that customer has left
    def customer_reviews(self):
        return [review for review in session.query(Review).filter(Review.id == self.id)]

    # return a collection of all the restaurants that the customer has reviewed
    def customer_restaurants(self):
        return self.restaurant

    # return the full name of the customer
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    # returns the restaurant instance that has the highest star rating from this customer
    def favorite_restaurant(self):
        return [session.query(Restaurant).filter(Restaurant.id == restaurant_id[0]).first() for restaurant_id in session.query(Review.restaurant_id).filter(Review.customer_id == self.id).order_by(Review.star_rating.desc()).limit(1)]
    
    # creates a new review for the restaurant with the given restaurant id
    def add_review(self, restaurant, rating):
        new_review = Review(
            customer_id = self.id, 
            restaurant_id = restaurant.id, 
            star_rating = rating
            )
        session.add(new_review)
        session.commit()

    # delete reviews
    def delete_reviews(self, restaurant):
        session.query(Review).filter_by(restaurant_id = restaurant.id, customer_id = self.id).delete()

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    star_rating = Column(Integer())
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    def __repr__(self):
        return f"review{self.id}: " \
            + f"star rating = {self.star_rating}, " \
            + f"restaurant_id = {self.restaurant_id}, " \
            + f"customer_id = {self.customer_id}"

    # create relationship
    restaurant_rv = relationship('Restaurant', back_populates='reviews')
    customer_rv = relationship('Customer', back_populates='reviews')

    # should return a collection of all the reviews that the customer has left
    def customer_review(self):
        return session.query(Customer).filter(Customer.id == self.customer_id).first()

    # return the restaurant instance for this review
    def restaurant_review(self):
        return session.query(Customer).filter(Customer.id == self.customer_id).first()
    
    def full_review(self):
        return f'Review for {self.restaurant_review()} by {self.customer_review().full_name()}: {self.star_rating} stars.'
