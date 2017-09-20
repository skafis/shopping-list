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
        self.shopping_list = []

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


class ShoppingList(object):
    id_index = dict()
    id_generator = itertools.count(1)  # first generated is 1

    def __init__(self, title, description):
        self.id = next(self.id_generator)
        self.title = title
        ShoppingList.id_index[self.id] = self
        self.users = []
        self.items = []
        self.shopping_list = {}
        self.last_list_id = 0

    def add_user(self, user):
        self.users.append(user)

    def add_items(self, items):
        self.items.append(items)

    def get_list(self):
        return self.shopping_list

    def add_list(self, slitst):
        self.last_list_id += 1
        self.shopping_list[self.last_list_id] = slitst
        slitst._id = self.last_list_id



    @classmethod
    def find_by_id(cls, id):
        return ShoppingList.id_index[id]

    @classmethod
    def delete_by_id(cls, id):
        del ShoppingList.id_index[id]
        
class Items(object):
    id_generator = itertools.count(1)  # first generated is 1

    def __init__(self, title, content, list_id):
        self.id = next(self.id_generator)
        self.title = title
        self.content = content
        self.status = False
        self.list_id = list_id