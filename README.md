# "There is no such thing as bad weather, only bad clothing."

<img src="https://github.com/NoelleinMN/goh/blob/master/static/images/GOH-logo.png" alt="GOH!" align="right"> 

## GOH...Get Out of the House!
Based on lessons learned during the global pandemic, "GOH!" (Get Out of the House) is designed to support users in getting outside to spend more time in nearby nature, parks, and recreation locations. GOH! allows users to create a profile with preferences, and then uses the robustness of the Google Maps API to return localized parks and recreation locations that may fit their needs and interests.

Return results include a user's personalized map with markers, location information, user rating, and a link to external details about the location. After completing a profile, users are able to safely and securely login/out and save locations to their favorites with immediate updates to their personalized favorites page. GOH! uses a PostgreSQL database to store user profile data, favorite parks, and API location details, and is built with a Python/Flask backend.

## About the Developer
GOH! was created by Noelle Notermann, a software engineer in Minnesota. After studying music, languages, and mathematics in college, she went on to earn graduate degrees in music performance and pedagogy, with focus areas in higher education administration and women in leadership. She volunteers as a conflict coach and facilitative mediator in the areas of social justice, DEI, and restorative community dialogues. A natural problem solver, Noelle began to see patterns in her vocations and avocations that could benefit from improved technologies, and thus started a journey of self study that led to a love of coding. Learn more about the developer at www.linkedin.com/in/noellenotermann.

## Deployment
<n/>[Deployed with AWS](http://100.26.108.130/)
<n/>
<n/>![alt text](https://github.com/NoelleinMN/goh/blob/master/static/images/GOH-error-handling.gif "GOH homepage gif")

## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Future State](#future)
* [Installation](#installation)
* [License](#license)

## <a name="tech-stack"></a>Technologies
* Python
* Flask
* JavaScript
* Jinja
* PostgreSQL
* SQLAlchemy
* HTML
* CSS
* Bootstrap
* jQuery
* AJAX
* JSON
* Python unittest module
* Google Maps API
* Google Places API
* Google Geocoding

## <a name="features"></a>Features

#### Homepage
Users login on the landing page. The navbar provides access to their account or to create a profile.

![alt text](https://github.com/NoelleinMN/goh/blob/master/static/images/GOH-homepage.png "GOH homepage")

#### Inspiration
A transparent modal pulls random inspirational quotes which refresh with each page change or reload; built with JavaScript.

![alt text](https://github.com/NoelleinMN/goh/blob/master/static/images/GOH-modal.png "GOH about modal")

#### Design Concept
Wanting users to feel as though there are no barriers between them and nature, the design of GOH! is light and transparent, even for error handling.

![alt text](https://github.com/NoelleinMN/goh/blob/master/static/images/GOH-error-handling.png "GOH design and error modal")

#### Featured Parks
Using a random query pulling results from the PostgreSQL database, visitors to the site can view maps of two "featured parks" which have been favorited by any user in the database.

![alt text](https://github.com/NoelleinMN/goh/blob/master/static/images/GOH-featured-parks.png "GOH featured parks")

#### User Profile
The user profile page is built with a transparent form (HTML and CSS), and includes error handling.

![alt text](https://github.com/NoelleinMN/goh/blob/master/static/images/GOH-profile-page.png "GOH! user profile")

## <a name="future"></a>Future State
GOH! has several features planned for the next sprint:
* More flexible search by keyword
* Add comments to favorites
* Include more local park information such as photos
* Add connection to weather API (Yahoo weather)
* OAuth for login

## <a name="installation"></a>Installation

Please follow these steps to run GOH! on your local device.

Clone repository:
    ```
    $ git clone https://github.com/NoelleinMN/goh.git
    ```

Get your own API key for Google Maps and save it to a file called <kbd>secrets.sh</kbd>. Your file should look something like this:
    ```
    export GOOGLE_MAPS_API_KEY='xyz123'   
    ```

Create a virtual environment:
    ```
    $ virtualenv env
    ```

Activate the virtual environment:
    ```
    $ source env/bin/activate
    ```

Source your keys from secrets.sh to your environment:
    ```
    $ source secrets.sh
    ```

Install dependencies:
    ```
    $ pip3 install -r requirements.txt
    ```

Create database 'goh':
    ```
    $ createdb goh
    ```

Create your database tables and seed example data:
    ```
    $ python3 seed_database.py
    ```

Run the app from the command line:
    ``` 
    $ python3 server.py
    ```

You can now navigate to 'localhost:5000/' to access GOH!


## <a name="license"></a>License
The MIT License (MIT) Copyright (c) 2021 Noelle Notermann

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.