"""Server for GOH!"""

from flask import (Flask, jsonify, render_template, request, flash, session,
                   redirect)
import requests
import json
from model import connect_to_db
import crud
import os

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "servertests"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['GOOGLE_MAPS_KEY']
GEOCODE_BASE_URL: "https://maps.googleapis.com/maps/api/geocode/json"



@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html', API_KEY=API_KEY)


@app.route('/users')
def all_users():
    """View all user profiles."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/login', methods=['POST'])
def user_login():
    """Check for user and allow login."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        if password == user.user_password:
            session['user_first_name'] = user.user_first_name    # not working on html page?
            session['user_email'] = user.user_email
            # print(user.user_first_name)
            # print(user.user_email)
            # print(session)
            return render_template('user_profile.html', user=user, API_KEY=API_KEY)           # correct this to go to a user's park and profile page
        else:
            flash('Email and password do not match. Try again.')
            return redirect ('/')
    else:
        flash('No user with that email. Please create a new profile.')
        return redirect ('/')


@app.route("/logout")
def user_logout():
    """Log out the current user and delete session information"""

    try:
        del session['user_email']
        del session['user_first_name']
    except KeyError:
        pass
    flash("You are logged out.")
    return redirect("/")


# @app.route('/login/favorites')  # throws error of assertionError conflict with all_favorites function (endpoint)
# def all_favorites():
#     """View all favorited parks."""
#     pass
    # favorites = crud.get_favorite_parks()

    # return render_template('all_favorited_parks.html', favorites=favorites)

@app.route('/api/add_favorite', methods=["POST"])
def add_favorite():
    
    fav_park_id = request.form.get("favParkId")
    user_email = session["user_email"]
    # fields = "address component"

    endpoint = "https://maps.googleapis.com/maps/api/place/details/json?"

    payload = {"place_id": fav_park_id,
                "key":API_KEY,
                "fields":"address_component,formatted_address,name"   #,geometry,icon,photo"
                }

    response = requests.get(endpoint, payload)
    data = response.json()
    print(data)
    park_street_address = data['result']['address_components'][0]['long_name'] + " " + data['result']['address_components'][1]['long_name'] #street address
    park_city = data['result']['address_components'][3]['long_name'] #city
    park_state = data['result']['address_components'][5]['short_name'] #state 2 ltr
    park_zipcode = data['result']['address_components'][7]['long_name'] #postal code
    park_name = data['result']['name'] # park name

    print(f"{park_street_address}, {park_city}, {park_state}, {park_zipcode}, {park_name}")
    # favorite_park = crud.create_favorite_park(fav_park_id, park_name, park_zipcode, park_street_address, park_city, park_state)

#use crud function to make user favorite and also add to user_fav database

    return "Saved to favorites"


@app.route('/login/map')
def show_user_map():

    if 'user_email' in session:
        return render_template('user_map.html', API_KEY=API_KEY)
    else:
        return redirect('/')


@app.route('/user_address.json')
def get_user_address():
    print(session)

    if 'user_email' in session:
        user = crud.get_user_by_email(session['user_email'])
        address = f'{user.user_street_address} {user.user_city}, {user.user_state} {user.user_zipcode}'
        return {'address': address}
    else:
        return {}


@app.route('/user_map.json')
def get_google_map_data():

    lat = request.args.get("lat")
    lng = request.args.get("lng")
    user = crud.get_user_by_email(session['user_email'])

    endpoint = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

    payload = {"query":f"{user.user_activity1} {user.user_activity2} {user.user_activity3}",
                "location":f"{lat},{lng}",
                "radius":user.max_search_distance,
                "type":"park",
                "key":API_KEY
                }

    response = requests.get(endpoint, payload)
    print(response.url)
    
    return response.json()


@app.route('/favorites')
def all_favorites():
    """View all favorited parks."""

    favorites = crud.get_favorite_parks()

    return render_template('all_favorited_parks.html', favorites=favorites)


@app.route('/parks/search')
def find_parks():
    """Search for parks based on zipcode in Google Maps query"""

    zipcode = request.args.get('zipcode', '')
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={zipcode}&key={API_KEY}'

    response = requests.get(url)
    data = response.json()      # does .load() to response to make it a python dictionary
    
    try:
        coords = data['results'][0]['geometry']['location']
    except IndexError:
        print('Item index does not exist')
    
    if data['status'] == "OK":
        print(data)
        return render_template('map_practice3.html',
                           data=data, zipcode=zipcode,
                           coords=coords, API_KEY=API_KEY)
    else:
        flash('Not a valid location. Please try again.')
        return redirect ('/')


@app.route('/newuser') #, methods=['POST'])
def create_user_profile():
    """Create a new user profile."""

    # email = request.form.get('email')
    # password = request.form.get('password')

    # user = crud.get_user_by_email(email)
    # if user:
    #     flash('Cannot create an account with that email. Try again.')
    # else:
    #     crud.create_user(email, password)
    #     flash('Account created! Please log in.')

    return render_template('setup_new_user.html')
    # return redirect('/')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
