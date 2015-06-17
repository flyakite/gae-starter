from base import AppTestCase
from models.user import User

class MyTestCase(AppTestCase):
    """
    Test example
    """
    def test_index(self):
        response = self.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html')
        self.assertIn('About', response)

    def test_signup(self):
        response = self.post('/', {
            'username': 'username',
            'password': 'password',
        }, csrf=True)

        self.assertEqual(response.status_code, 200)
        user = User.query(User.username == 'username').fetch()
        self.assertTrue(user)