import unittest
from users import User
from app import create_account

class UserManagementTestcase(unittest.TestCase):
    '''
    the class contains the test cases for signing in
    and signing up
    '''

    def setUp(self):
        '''
        initilize the test
        '''
      
        self.users_db = User()


    def test_create_account(self):
        '''
        test creating of accounts
        '''
        # self.users_db = User()
        new_user = self.users_db.create_accounts('admin', 'password')
        self.assertTrue(new_user.check_user('admin'))

    def test_login(self):
        '''
        test if login works
        '''
        # self.users_db = User()
        self.users_db.create_accounts('admin', 'password')
        self.assertTrue(self.users_db.verify_password('admin', 'password'))

    def test_failed_login(self):
        '''
        test if login will fail
        '''
        # self.users_db = User()
        self.users_db.create_accounts('admin', 'password')
        self.assertFalse(self.users_db.verify_password('admin', 'anewpassword'))

    def test_duplicate_users(self):
        '''
        test if it will find duplicate users
        '''
        self.users_db.create_accounts('admin', 'password')
        self.assertIn('admin', self.users_db.create_accounts('admin', 'password'))
        




if __name__ == '__main__':
    unittest.main()