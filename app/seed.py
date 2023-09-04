from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Restaurant, Customer, Review

fake = Faker()

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///restaurant.db')
    Session = sessionmaker(bind=engine)
    session = Session()

# Clear our database before each new seed 
# session.query(Restaurant).delete()
# session.commit()