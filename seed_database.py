"""Script to seed database with sample data."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server


os.system('dropdb goh')
os.system('createdb goh')

model.connect_to_db(server.app)
model.db.create_all()


'''Create sample data for use with GOH! project database.'''

def example_data():
    """Create some sample data."""

    # Add sample parks
    como = crud.create_favorite_park(park_API_id=120, park_name='Como Lake Park', park_zipcode=55117, 
            park_street_address='12 Como Ave', park_city='St Paul', park_state='MN')
    north_dale = crud.create_favorite_park(park_API_id=317, park_name='North Dale Rec Center', park_zipcode=55114, 
            park_street_address='233 Cottage St', park_city='St Paul', park_state='MN')
    lexington = crud.create_favorite_park(park_API_id=908, park_name='Lexington Park', park_zipcode=55113, 
            park_street_address='1906 Lexington Ave N', park_city='Roseville', park_state='MN')

    # Add sample parks and user key that have been favorited by a user (Association table)
    # fav1 = User_Favorite() # what is needed to create this data since it is PK and FK only?
    # no data for fav1; consider in Phase 2.

    # Add sample users
    quanisha = crud.create_user(user_email='quanisha@gmail.com', user_password='test123', user_first_name='Quanisha', 
                 user_zipcode=55113, user_city='St Paul', user_activity1='swim', user_activity2='bike',
                 family_friendly=1, children_toddler=1, user_last_name='Anderson', user_street_address='13 Albert St',
                 user_state='MN', user_activity3='walk', max_search_distance=5, pet_friendly=1, accessibility_needs=1,
                 amenities1='restroom', amenities2='shelter', children_teen=1, children_schoolage=0, children_infant=1)
    gabriella = crud.create_user(user_email='gabriella@gmail.com', user_password='fake123', user_first_name='Gabriella', 
                 user_zipcode=91140, user_city='Sacramento', user_state='CA', user_last_name='Best', user_activity1='run', 
                 user_activity2='bike', user_activity3='sunbathing', max_search_distance=10, family_friendly=0,
                 pet_friendly=1, children_infant=1, children_schoolage=1, children_teen=0, children_toddler=0,
                 user_street_address='3442 Woodlane Park', accessibility_needs=0, amenities2='restroom', amenities1='kiosk')
    nicole = crud.create_user(user_email='nicole@gmail.com', user_password='pass123', user_first_name='Nicole', 
                user_last_name='Driver', user_street_address='123 St Albans', user_zipcode=55113, 
                user_city='St Paul', user_state='MN', user_activity1='swim', user_activity2='bike',
                user_activity3='walk', max_search_distance=50, pet_friendly=1, accessibility_needs=1,
                family_friendly=1, amenities1='restroom', amenities2='shelter', children_teen=1, children_toddler=1, 
                children_schoolage=0, children_infant=1)
    queentesa = crud.create_user(user_email='queentesa@gmail.com', user_password='login123', user_first_name='Queentesa', 
                user_zipcode=55117, user_city='Roseville', user_activity1='walk', pet_friendly=1, user_state='MN',
                children_toddler=1, amenities1='restroom', amenities2='shelter', user_last_name='Strong', children_teen=0,
                user_street_address='996 Montana Ave', user_activity2='sunbathing', user_activity3='bike', children_infant=1,
                children_schoolage=0, max_search_distance=30, family_friendly=1, accessibility_needs=0)


    model.db.session.add_all([como, north_dale, lexington, quanisha, gabriella, nicole, queentesa])
    model.db.session.commit()


example_data()
