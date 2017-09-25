import os
import flask
import unittest
from main import create_account
from app import product

app = flask.Flask(__name__)

class ShoppingAppTestCase(unittest.TestCase):
    def set_up(self):
        self.create_account = create_account
        self.list_view = 


    def test_sign_up(self, username, email, password):
    	return self.create_account.post('/sign-up', data=dict(
    		username=username,
    		email=email,
    		password=password), follow_redirect=True)



if __name__ == '__main__':
    unittest.main()