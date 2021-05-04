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


@app.route('/home')
def test_home():
    return render_template('test_homepage.html')


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html', API_KEY=API_KEY)


@app.route('/about')
def view_about():
    """View about page."""

    return render_template('about_goh.html')

@app.route('/users')
def all_users():
    """View all user profiles."""

    users = crud.get_users()                                #pragma: no cover

    return render_template('all_users.html', users=users)   #pragma: no cover


@app.route('/login', methods=['POST'])
def user_login():
    """Check for user and allow login."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        if password == user.user_password:
            session['user_first_name'] = user.user_first_name
            session['user_email'] = user.user_email
            # print(user.user_first_name)
            # print(user.user_email)
            # print(session)
            return redirect('/login/map')    
        else:
            flash('Email and password do not match. Try again.')
            return redirect ('/')
    else:
        flash('No user with that email. Please create a new profile.')
        return redirect ('/')

@app.route('/login/profile')
def view_profile():
    """View user profile once logged in."""

    if 'user_email' in session:
        user = crud.get_user_by_email(session['user_email'])
        return render_template('user_profile.html', user=user, API_KEY=API_KEY)
    else:
        flash('Please sign in to your account.')
        return redirect('/')

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


@app.route('/login/user_favorites')
def user_favorites():
    """View all favorited parks."""

    if 'user_email' in session:
        user = crud.get_user_by_email(session['user_email'])
        user_email = session['user_email']
        favorites = crud.get_user_fav(user_email)
        return render_template('user_favorite_parks.html', user=user, favorites=favorites, API_KEY=API_KEY)
    else:
        flash("Please sign in to your account.")
        return redirect('/')


@app.route('/api/add_favorite', methods=["POST"])
def add_favorite():
    
    fav_park_id = request.form.get("favParkId")
    user_email = session["user_email"]

    data = get_fav_data_api(fav_park_id)

    park_address = data['result']['formatted_address'] #street address
    park_name = data['result']['name'] # park name
    # pic_height = data['photos']['photo_reference']
    # pic_ref = data['photos'][0]
    
    print(f"{park_address}, {park_name}")
    favorite_park = crud.create_favorite_park(fav_park_id, park_name, park_address)
    user_fav_park = crud.create_user_fav(fav_park_id, user_email)

    return "Saved to favorites"   

def get_fav_data_api(fav_park_id):
    
    endpoint = "https://maps.googleapis.com/maps/api/place/details/json?"

    payload = {"place_id": fav_park_id,
                "key":API_KEY,
                "fields":"formatted_address,name,photos"   #,geometry,icon,photos"
                }

    response = requests.get(endpoint, payload)
    data = response.json()
    # print(response.url)
    # print(data)

    return data



@app.route('/login/map')
def show_user_map():

    if 'user_email' in session:
        user = crud.get_user_by_email(session['user_email'])
        return render_template('user_map.html', user=user, API_KEY=API_KEY)
    else:
        flash("Please sign in to your account.")
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


@app.route('/all_favorites')
def all_featured_favorites():
    """View featured favorited parks."""

    favorites = crud.get_featured_parks()

    return render_template('all_favorited_parks.html', favorites=favorites, API_KEY=API_KEY)


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
        return render_template('map_search_by_zip.html',
                           data=data, zipcode=zipcode,
                           coords=coords, API_KEY=API_KEY)
    else:
        flash('Not a valid location. Please try again.')
        return redirect ('/')


@app.route('/newuser', methods=['GET','POST'])
def create_user_profile():
    """Create a new user profile."""

    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        user_first_name = request.form.get('user_first_name')
        user_last_name = request.form.get('user_last_name')
        user_street_address = request.form.get('user_street_address')
        user_city = request.form.get('user_city')
        user_zipcode = int(request.form.get('user_zipcode'))
        user_state = request.form.get('user_state')
        user_activity1 = request.form.get('user_activity1')
        user_activity2 = request.form.get('user_activity2')
        user_activity3 = request.form.get('user_activity3')
        max_search_distance = int(request.form.get('max_search_distance'))
        amenities1 = request.form.get('amenities1')
        amenities2 = request.form.get('amenities2')
        pet_friendly = bool(int(request.form.get('pet_friendly')))
        accessibility_needs = bool(int(request.form.get('accessibility_needs')))
        family_friendly = bool(int(request.form.get('family_friendly')))
        children_infant = bool(int(request.form.get('children_infant')))
        children_toddler = bool(int(request.form.get('children_toddler')))
        children_schoolage = bool(int(request.form.get('children_schoolage')))
        children_teen = bool(int(request.form.get('children_teen')))
        
        user = crud.get_user_by_email(user_email)
        if user:
            flash('Account already created with that email. Please login or try another email.')
            return redirect('/')

        else:
            user = crud.create_user(user_email, user_password, user_first_name, user_last_name, user_zipcode,
                                    user_street_address, user_city, user_state, user_activity1, user_activity2,
                                    user_activity3, max_search_distance, pet_friendly, family_friendly,
                                    accessibility_needs, amenities1, amenities2, children_infant, children_toddler, children_schoolage, children_teen)
            flash('Account created! Please log in.')
            return redirect('/')
    
    elif request.method == 'GET':
        return render_template('setup_new_user.html')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
