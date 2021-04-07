"""Models for GOH...Get Out of the House!"""
# db name = goh

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User profile information."""

    __tablename__ = 'user_profiles'

    user_email = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    user_password = db.Column(db.String, nullable=False)
    user_first_name = db.Column(db.String, nullable=False)
    user_last_name = db.Column(db.String)
    user_zipcode = db.Column(db.Integer, nullable=False)
    user_street_address = db.Column(db.String)
    user_city = db.Column(db.String)
    user_state = db.Column(db.String) # how to limit to two character abbreviation?
    user_activity1 = db.Column(db.String)
    user_activity2 = db.Column(db.String)
    user_activity3 = db.Column(db.String)
    max_search_distance = db.Column(db.Integer)
    pet_friendly = db.Column(db.Boolean, default=False) 
    family_friendly = db.Column(db.Boolean, default=False)
    accessibility_needs = db.Column(db.Boolean, default=False)
    amenities1 = db.Column(db.String)
    amenities2 = db.Column(db.String)
    children_infant = db.Column(db.Boolean, default=False)
    children_toddler = db.Column(db.Boolean, default=False)
    children_schoolage = db.Column(db.Boolean, default=False)
    children_teen = db.Column(db.Boolean, default=False)

    # user_favorites: an association table of User_Favorite objects with user_email and park_API_id

    def __repr__(self):
        return f'<User: {self.user_first_name} Email: {self.user_email}>'


class Favorite_Park(db.Model):
    """Favorite park information."""

    __tablename__ = 'favorite_parks'

    park_API_id = db.Column(db.Integer, primary_key=True) # get from API
    park_name = db.Column(db.String)
    park_zipcode = db.Column(db.Integer)
    park_street_address = db.Column(db.String)
    park_city = db.Column(db.String)
    park_state = db.Column(db.String)

    # user_favorites: an association table of User_Favorites with user_email and park_API_id

    def __repr__(self):
        return f'<Favorite Park Added: {self.park_name} API ID: {self.park_API_id}>'


class User_Favorite(db.Model):
    """Association table of user favorites."""

    __tablename__ = 'user_favorites'

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_API_id = db.Column(db.Integer, db.ForeignKey('favorite_parks.park_API_id'))
    user_email = db.Column(db.String, db.ForeignKey('user_profiles.user_email'))

    favorite_park = db.relationship('Favorite_Park', backref='user_favorites')
    user = db.relationship('User', backref='user_favorites')

    def __repr__(self):
        return f'<User favorited: {self.park_API_id} User email: {self.user_email}>'


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    User_Favorite.query.delete()
    Favorite_Park.query.delete()

    # Add sample users, parks, and favorites
    como = Favorite_Park(park_API_id=120, park_name='Como Lake Park', park_zipcode=55117, 
            park_street_address='12 Como Ave', park_city='St Paul', park_state='MN')
    north_dale = Favorite_Park(park_API_id=317, park_name='North Dale Rec Center', park_zipcode=55114, 
            park_street_address='233 Cottage St', park_city='St Paul', park_state='MN')
    lexington = Favorite_Park(park_API_id=908, park_name='Lexington Park', park_zipcode=55113, 
            park_street_address='1906 Lexington Ave N', park_city='Roseville', park_state='MN')

    #fav1 = User_Favorite() # what is needed to create this data since it is PK and FK only?

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


def connect_to_db(flask_app, db_uri='postgresql:///goh', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if program output gets too annoying; 
    # this will tell SQLAlchemy not to print out every query it executes.

    connect_to_db(app)
