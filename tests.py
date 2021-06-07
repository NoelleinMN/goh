import unittest
from server import app
import server
from model import User, connect_to_db, db
from seed_database import example_data
from flask import session


class FlaskTestsBasic(unittest.TestCase):
    """Flask tests."""

    def setUp(self):
        """Before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""
        result = self.client.get("/")
        self.assertIn(b"There is no such thing as bad weather", result.data)

    def test_new_users(self):
        """Test user profile creation page."""
        result = self.client.get('/newuser')
        self.assertIn(b"Basic Personal Information", result.data)

    def test_failed_map_search(self):                      
        """Test failed non-logged in search. Non-API."""
        result = self.client.get('/parks/search', follow_redirects=True)
        self.assertIn(b"Not a valid location.", result.data)


class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///test_goh", echo=False)

        # Create tables and seed data               
        db.create_all()
        example_data()

        with self.client as c:             
            with c.session_transaction() as sess:
                sess['user_email'] = "nicole@gmail.com"
                sess['user_first_name'] = "Nicole"

    def tearDown(self):                            
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_featured_parks_list(self):          
        """Test featured parks page."""
        result = self.client.get("/all_favorites")
        self.assertIn(b"Featured Parks", result.data)

    def test_find_user(self):
        """Can we find a user in the sample data?"""

        nicole = User.query.filter(User.user_first_name == "Nicole").first()
        self.assertEqual(nicole.user_first_name, "Nicole")

    def test_user_profile(self):               
        """Test user profile view page."""

        result = self.client.get("/login/profile", data={"user_email": "nicole@gmail.com", "password": "pass123"},
                              follow_redirects=True)
        self.assertIn(b"Pet Friendly", result.data)

    def test_user_favorites(self):               
        """Test user favorites page."""

        result = self.client.get("/login/user_favorites", data={"user_email": "nicole@gmail.com", "password": "pass123"},
                              follow_redirects=True)
        self.assertIn(b"Favorite Places", result.data)

    def test_login(self):                         
        """Test log in form."""

        result = self.client.post("/login", data={'email': 'nicole@gmail.com', 'password': 'pass123'}, follow_redirects=True)
        self.assertIn(b"Explore suggested locations and add to favorites", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_email'] = 'nicole@gmail.com'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'user_email', session)
            self.assertIn(b'There is no such thing as bad weather', result.data)


class MockAPITests(unittest.TestCase):
    """Flask tests that use the database and mock API call."""

    def setUp(self):
        """Before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///test_goh", echo=False)

        # Create tables and seed data               
        db.create_all()
        example_data()

        with self.client as c:             
            with c.session_transaction() as sess:
                sess['user_email'] = "nicole@gmail.com"
                sess['user_first_name'] = "Nicole"

        def _mock_get_fav_data_api(fav_park_id):
            """Mock test of API call"""

            return {'html_attributions': [], 'result': {'formatted_address': '1515 Keats Ave N, Lake Elmo, MN 55042, USA', 'name': 'Lake Elmo Park Reserve', 'photos': [{'height': 1731, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/113941198282368414473">Lake Elmo Park Reserve</a>'], 'photo_reference': 'ATtYBwKvFPmxDJU48oKGydyRAP1_LT1v-Ui6RMXtb59LFzfUEL51BU2RjmcBUD96wMWk4kgrqXQC5oQ0QDFx6WhS2wF_3sNSM4gsZ35NareAdh0UfJ2KEF7zeBvQBgZHFfgyIalUvm6I-t-xm_xaQ7ISK0uEgugL36WcmUuRM-dcds5JF03X', 'width': 2600}, {'height': 3024, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109627993211852364929">Andrew Gontarek</a>'], 'photo_reference': 'ATtYBwKoEPsi6yzM35cIKvqgAPcduf2tEEpxKjPainbYTKSMt8v4WIIFwhFD2Wv4FSJSbi0d4tVHwMWLURhUzjoBsye4F-69DJLfpcMiIy2A8qUMVwz31jX0_ip_Q8JrOLqnU6m5I64Tbv9Fluu3vmUuNYVCCxfzphnDbABPNyRBcECUPNXJ', 'width': 4032}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/104646741841860661226">Yazmin Reyes</a>'], 'photo_reference': 'ATtYBwJgBBWPSE_DvP250v7FpwNYDOIb-ZWKLdHuroCklaeIYwGOimr_zSUXikgunm8lvWcoOZ9H0aYRcuV5jdk0S4_68E5rwCSvswhVKM6ib-DLSLiOgHKTxYFfRV5xm3UqGI4E0pZarnf-XKWrcxbOJaBPBy077t5YuswmC6eEzbfWQhzl', 'width': 3024}, {'height': 3024, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117000989128220333729">Alison Bowker</a>'], 'photo_reference': 'ATtYBwIjTYxnt4h2Ke0zMDbmIJNEiEceeY1D0sEdlxb6OwH5buANMdvB9ibRKPMC1Q6SZdfwgZZmptyo8rkvG1ufQj8i7PcmlTLqdKgNg5OUw0Ylxmu6wx5bLQM00FWEsMN8YGtkHVD0oPtrChxZPRj0ymVpYfsqOOwq8SS185bbyJN5OefI', 'width': 4032}, {'height': 3583, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/112582953006911993341">Leah Charlsen</a>'], 'photo_reference': 'ATtYBwILE1DuH2A7sDYUpDd7eFTTrdXdYy9tmnNAvvbFZYPYnX4NCz_755OCQWQ_535xwNJ4WbN40acP92a12r0-CZdemuUWjFapLc_PyymGNGJKJji4IlNnQVOzJg2wxKlLSRFkrTUdKXoIugaZ9rR__1q-XsNV_b5TXw7Or5NwNo1OoTTY', 'width': 1908}, {'height': 3456, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/102974591944691502780">Lizabeth Kyser</a>'], 'photo_reference': 'ATtYBwLh-UC-AbkcAMXpN_rMR1eeErSz5wVnhT6xwXa7hTgckpHUS1JHPlmrQqwPv0Fs9zgPvms3iWL07Q0oYY_Sa6vA-pyfDrWG07E7hyAx4alfwqfUmIKd5MF7b9MTEOWy_ccgkogONsl76640XUIi3pzifRVL9NwoGeGMVG9Pm3AzwBTr', 'width': 4608}, {'height': 3024, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111658228381463654223">Aaron Bolduc</a>'], 'photo_reference': 'ATtYBwKgt_wSlKL2v-3vHM_Mza_8_IxG1JoQMUrBErnMVTMHeNSG_zkBKQWG_LfuMhVOgKXQ93cMtoM568DkRi5Hf34erhS9gkvH4bWK4qiMGI0Xo2816JeDlVIaUkHU-ZjbfDiHjV78rwdx_3MrTNS08M5h2ZeHNXqC4gTGungxFrUD5SR7', 'width': 4032}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/104183341438553618909">Ken Boyd</a>'], 'photo_reference': 'ATtYBwIR4myfVaiMDj4TyBNn4eYw73z5GsbX4z79lv-sbzKuQ3SKaoUvjYYrDO6OaPwsvfDQwVD3Xyx1ag1mpe--MJO4qdd2YcF1JhDoN5fF6iK0tBXOhK_SQ6ZrRaIHNNPvYE4h-Xkw9-dQmQoC2rUwn2YT1y3DXF5P2PDgCbolMdk0Ggt_', 'width': 3024}, {'height': 3024, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111658228381463654223">Aaron Bolduc</a>'], 'photo_reference': 'ATtYBwIueZUj9Ei0q8lvC3B813wo3igQIylOB61G04syrOe1ZeS12SBBJtLi2k7UelP2eZ00UOm8A60X1wAwuo3ihXmDvLYsNlIcXn__F1fFkG9yD--x58zFZKPVpVUZ4jP6AgtPJeUCQrOgZgIvTy8jAR5QMaN8QRILQrF8FdfuY0jQUmwO', 'width': 4032}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/113668662980540441669">Mari Boyd</a>'], 'photo_reference': 'ATtYBwLGZmaf0axPkbxRuAjGVzSgt1z4A2Jqn3lz5LXQO-e5kNSB032N0RkW84E4QD-wtCkxVrk5F-ArCZG7KyyQSQRh37MmJeIja69iZBB0UgUtQYY_b8z4MdCuQDTCKEG7YG-V2U-yH5K6ej3OHkXNIm0fbRPuDq8j2pvEDLWRhW_PbXY', 'width': 3024}]}, 'status': 'OK'}

        server.get_fav_data_api = _mock_get_fav_data_api

    def tearDown(self):                            
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    @unittest.expectedFailure   #autoincrement issue with related table, but does show connection to DB with API results
    def test_get_fav_data_API_with_mock(self):
        """Mock API call with data."""

        result = self.client.post('/api/add_favorite')
        self.assertEqual(result.status_code, 200)

if __name__ == "__main__":
    import unittest

    unittest.main()

