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


@app.route('/favorites')
def all_favorites():
    """View all favorited parks."""

    favorites = crud.get_favorite_parks()

    return render_template('all_favorited_parks.html', favorites=favorites)


# @app.route('/favorites/<park_API_id>')
# def show_movie(movie_id):
#     """Show details on a particular movie."""

#     movie = crud.get_movie_by_id(movie_id)

#     return render_template('movie_details.html', movie=movie)


@app.route('/users')
def all_users():
    """View all user profiles."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


# @app.route('/users', methods=['POST'])
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


@app.route('/users/<user_email>')
def show_user_profile(user_id):
    """Show profile of a specific user by email."""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
