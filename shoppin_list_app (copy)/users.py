from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, password):
        self.accounts_db = {}
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active

    def create_accounts(self, username, password):
        self.accounts_db['username'] = password

    def check_user(self, username):
        if username in accounts_db.keys():
            return True
        else:
            return False

    def verify_password(self, username, password):
        if accounts_db['username'] == password:
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
