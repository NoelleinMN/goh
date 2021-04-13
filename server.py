"""Server for GOH!"""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "servertests"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/users')
def all_users():
    """View all user profiles."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/login')
def show_login_page(user_email):
    """Show page for specific user with parks."""

    # user = crud.get_user_by_email(user_email)
    parks = crud.get_parks_by_user_zipcode(user_zipcode)

    return render_template('user_login_page.html', parks=parks)


@app.route('/login/<user_email>')
def show_user_profile(user_email):
    """Show profile of a specific user by email."""

    user = crud.get_user_by_email(user_email)

    return render_template('user_profile.html', user=user)


@app.route('/favorites')
def all_favorites():
    """View all favorited parks."""

    favorites = crud.get_favorite_parks()

    return render_template('all_favorited_parks.html', favorites=favorites)


# @app.route('/newaccount', methods=['POST'])
# def create_user_profile():
#     """Create a new user profile."""

#     email = request.form.get('email')
#     password = request.form.get('password')

#     user = crud.get_user_by_email(email)
#     if user:
#         flash('Cannot create an account with that email. Try again.')
#     else:
#         crud.create_user(email, password)
#         flash('Account created! Please log in.')

#     return redirect('/')


# @app.route('/favorites/<park_API_id>')
# def show_movie(movie_id):
#     """Show details on a particular movie."""

#     movie = crud.get_movie_by_id(movie_id)

#     return render_template('movie_details.html', movie=movie)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
