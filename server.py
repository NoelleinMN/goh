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


@app.route('/login/parks')
def show_login_page():  #user_email):
    """Show page for specific user with parks."""

    user = crud.get_user_by_email(session['user_email'])
 
    if user:
        # print(session)
        return render_template('user_parks.html', user=user, API_KEY=API_KEY)


@app.route('/login/<user_email>')
def show_user_profile(user_email):
    """Show profile of a specific user by email."""

    user = crud.get_user_by_email(user_email)

    return render_template('user_profile.html', user=user, API_KEY=API_KEY)


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

@app.route('/map')
def map_search():
    """View local park maps."""

    return render_template('map_practice3.html', API_KEY=API_KEY)


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
