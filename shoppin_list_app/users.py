from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    '''
    This class inherits from the user mixin and is responsible
    the user methods
    '''
    def __init__(self, username=None, password=None):
        self.accounts_db = {}
        self.username = username
        self.password = password
        self.active = True

        

    @property
    def is_active(self):
        return self.active


    def create_accounts(self, username, password):
        '''
        This method takes in username as the key and password 
        as the value
        '''
        self.accounts_db[username] = password
       
        return self

    def check_user(self, username):
        '''
        This method takes in a username and
        checks if its in the dictonary
        '''
        if username in self.accounts_db.keys():
            return True
        else:
            return False

    def verify_password(self, username, password):
        '''
        This method takes a username and password
        and verify if they match
        '''
        if self.accounts_db[username] == password:
            return True
        else:False

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    




def get_user(user_id):
    password = current_app.config['PASSWORDS'].get(user_id)
    user = User(user_id, password) if password else None
    if user is not None:
        user.is_admin = user.username in current_app.config['ADMIN_USERS']
    return user
