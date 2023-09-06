from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Restaurant, Customer, Review

fake = Faker()

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///restaurant.db')
    session = sessionmaker(bind=engine)
    session = session()

# Clear our database before each new seed 
    # session.query(Restaurant).delete()
    # session.query(Customer).delete()
    # session.query(Review).delete()

    customer_list=[]
    for i in range(20):
        customer = Customer(
            first_name = fake.first_name(),
            last_name = fake.last_name()
        )
        session.add(customer)
        session.commit()
        customer_list.append(customer)

    restaurant_list=[]
    for i in range(20):
        restaurant = Restaurant(
            name = fake.name_nonbinary(),
            price = random.randint(100,4000)
        )
        session.add(restaurant)
        session.commit()
        restaurant_list.append(restaurant)

    review_list=[]
    for customer in customer_list:
        for i in range(random.randint(1, 3)):
            restaurant = random.choice(restaurant_list)
            review = Review(
                star_rating = random.randint(1, 3),
                restaurant_id = restaurant.id,
                customer_id = customer.id
            )
            session.add(review)
            session.commit()
            review_list.append(review)  
    
    # Test Examples
    for i in range(2):
        print("Fanciest restaurant:",restaurant_list[i].fanciest())
        print("Customer full name", customer_list[i].full_name())
        print("Customer favourite restaurant:", customer_list[i].favorite_restaurant())
        print("Customer Reviews:", customer_list[i].customer_reviews())
        print("Customer reviewed restaurants:", customer_list[i].customer_reviews())
        print("Highest star rating restaurant:",customer_list[i].favorite_restaurant())
session.close()