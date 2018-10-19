from app import app
import unittest

class FlaskTestCase(unittest.TestCase):

    # Ensure flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure login works as expected given correct credentials
    def test_login_with_correct_credentials(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'You were logged in successfully', response.data)

    # Ensure login works as expected given incorrect credentials
    def test_login_with_incorrect_credentials(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="test", password="test"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentials. Please try again.', response.data)

    # Ensure logout works as intended
    def test_logout_successful(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)                
        self.assertIn(b'You successfully logged out', response.data)
        
    # Ensure main page requires login
    def test_main_route_login_required(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'Only for authorised users. Please log in.' in response.data)


    # Ensure logout page requires you to be logged in
    def test_logout_page_requires_logged_in(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'Only for authorised users. Please log in.' in response.data)

    # Ensure posts load on main page
    def test_main_page_posts_load(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Hello from the shell', response.data)


if __name__ == '__main__':
    unittest.main()