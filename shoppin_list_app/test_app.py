import unittest
from users import User

class UserManagementTestcase(unittest.TestCase):

    def setup(self):
        self.users_db = User()
        self.user_acc = {'username': 'admin', 'password': 'password'}


    def test_create_account(self):
        self.users_db = User()
        new_user = self.users_db.create_accounts('admin', 'password')
        self.assertTrue(new_user.check_user('admin'))

    def test_login(self):
        self.users_db = User()
        self.users_db.create_accounts('admin', 'password')
        self.assertTrue(self.users_db.verify_password('admin', 'password') )

    def test_failed_login(self):
        self.users_db = User()
        self.users_db.create_accounts('admin', 'password')
        self.assertFalse(self.users_db.verify_password('admin', 'anewpassword'))



if __name__ == '__main__':
    unittest.main()