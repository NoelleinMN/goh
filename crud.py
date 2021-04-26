"""CRUD operations."""

from model import db, User, Favorite_Park, User_Favorite, connect_to_db


def create_user(user_email, user_password, user_first_name, user_last_name, user_zipcode, user_street_address,
                user_city, user_state, user_activity1, user_activity2, user_activity3, max_search_distance,
                pet_friendly, family_friendly, accessibility_needs, amenities1, amenities2, children_infant,
                children_toddler, children_schoolage, children_teen):
    """Create and return a new user."""

    user = User(user_email=user_email, user_password=user_password, user_first_name=user_first_name,
            user_last_name=user_last_name, user_zipcode=user_zipcode, user_street_address=user_street_address,
            user_city=user_city, user_state=user_state, user_activity1=user_activity1, user_activity2=user_activity2,
            user_activity3=user_activity3, max_search_distance=max_search_distance, pet_friendly=pet_friendly,
            family_friendly=family_friendly, accessibility_needs=accessibility_needs, amenities1=amenities1,
            amenities2=amenities2, children_infant=children_infant, children_toddler=children_toddler,
            children_schoolage=children_schoolage, children_teen=children_teen)

    db.session.add(user)
    db.session.commit()

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_email(user_email):
    """Return a user by primary key."""

    return User.query.get(user_email)


def get_user_by_zipcode(user_zipcode):
    """Return users by zipcode."""

    return User.query.filter(User.user_zipcode == user_zipcode).all()


def create_favorite_park(park_API_id, park_name, park_zipcode, park_street_address, park_city, park_state):
    """Create and return a newly favorited park."""

    favorite_park = Favorite_Park(park_API_id=park_API_id, park_name=park_name,
                    park_zipcode=park_zipcode, park_street_address=park_street_address,
                    park_city=park_city, park_state=park_state)

    db.session.add(favorite_park)
    db.session.commit()

    return favorite_park


def get_favorite_parks():
    """Return all favorite parks."""

    return Favorite_Park.query.all()


def get_favorite_park_by_id(park_API_id):
    """Return a favorited park by primary key."""

    return Favorite_Park.query.get(park_API_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
