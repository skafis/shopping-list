import unittest
from users import User

class UserManagementsTestcase(unittest.TestCase):

    def setup(self):

        self.user_db = User

        self.user_acc = {'username': 'admin', 'password': 'password'}
        print (self.user_acc)


    def test_create_account(self):
        self.user_acc = {'username': 'admin', 'password': 'password'}
        self.user_db = User
        name = self.user_acc.get('username')
        pas = self.user_acc.get('password')
        new_user = self.user_db(name, pas)
        add_user = new_user.create_accounts(name, pas)
        self.assertTrue(add_user.check_user('admin'))

    # def test_if_user_exists(self):
    #     self.user_db = User
    #     self.user_acc = {
    #         'username': 'admin',
    #         'password': 'password'
    #     }
    #     user = self.user_acc.get('username')
    #     self.assertTrue(self.user_db.check_user(user), 'admin')

    
    	
    # def test_sign_up(self, username, email, password):
    # 	return self.create_account.post('/sign-up', data=dict(
    # 		username=username,
    # 		email=email,
    # 		password=password), follow_redirect=True)



if __name__ == '__main__':
    unittest.main()