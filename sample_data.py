'''Create sample data for use with GOH! project database.'''

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    # User.query.delete()
    # User_Favorite.query.delete()
    # Favorite_Park.query.delete()

    # Add sample parks
    como = Favorite_Park(park_API_id=120, park_name='Como Lake Park', park_zipcode=55117, 
            park_street_address='12 Como Ave', park_city='St Paul', park_state='MN')
    north_dale = Favorite_Park(park_API_id=317, park_name='North Dale Rec Center', park_zipcode=55114, 
            park_street_address='233 Cottage St', park_city='St Paul', park_state='MN')
    lexington = Favorite_Park(park_API_id=908, park_name='Lexington Park', park_zipcode=55113, 
            park_street_address='1906 Lexington Ave N', park_city='Roseville', park_state='MN')

    # Add sample parks and user key that have been favorited by a user (Association table)
    # fav1 = User_Favorite() # what is needed to create this data since it is PK and FK only?
    # no data for fav1; consider in Phase 2.

    # Add sample users
    quanisha = User(user_email='quanisha@gmail.com', user_password='test123', user_first_name='Quanisha', 
                user_zipcode=55113, user_city='St Paul', user_activity1='swim', user_activity2='bike',
                family_friendly=1, children_toddler=1)
    gabriella = User(user_email='gabriella@gmail.com', user_password='fake123', user_first_name='Gabriella', 
                user_zipcode=91140, user_city='Sacramento', user_activity1='run', user_activity2='bike',
                pet_friendly=1, children_infant=1)
    nicole = User(user_email='nicole@gmail.com', user_password='pass123', user_first_name='Nicole', 
                user_last_name='Driver', user_street_address='123 St Albans', user_zipcode=55113, 
                user_city='St Paul', user_state='MN', user_activity1='swim', user_activity2='bike',
                user_activity3='walk', max_search_distance=50, pet_friendly=1, accessibility_needs=1,
                family_friendly=1, amenities1='restroom', children_teen=1)
    queentesa = User(user_email='queentesa@gmail.com', user_password='login123', user_first_name='Queentesa', 
                user_zipcode=55117, user_city='Roseville', user_activity1='walk', pet_friendly=1, 
                children_toddler=1, amenities1='restroom', amenities2='shelter')


    db.session.add_all([como, north_dale, lexington, quanisha, gabriella, nicole, queentesa])
    db.session.commit()