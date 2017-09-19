from flask import Flask
from flask_bcrypt import Bcrypt
from collections import defaultdict
from datetime import datetime
import itertools

app = Flask(__name__)
app.secret_key = 'asdfzxcvqwer'
bcrypt = Bcrypt(app)

class User(object):
    email_index = dict()

    def __init__(self, user_name, email, user_password):
        self.user_name = user_name
        self.email = email
        self.user_password = self.set_password(user_password)
        self.authenticated = False
        User.email_index[email]= self

    @classmethod
    def find_by_email(cls, email):
        return User.email_index[email]

    def set_password(self, password):
        return bcrypt.generate_password_hash(password)

    def is_active(self):
        # make all user active
        return True

    def get_id(self):
        # return email adress for flask login
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def check_password(self, hashed_password, password):
        # return true or false
        return bcrypt.check_password_hash(hashed_password, password)

    def is_anonymous(self):
        # Dont support anonymus users
        return False


