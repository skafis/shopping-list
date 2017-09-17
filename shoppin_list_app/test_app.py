import os
import main
import unittest
import tempfile

class ShoppingAppTestCase(unittest.TestCase):
    def set_up(self):
        main.testing = True
        self.app = main.test_client()

    def test_sign_up(self):     
        rv = self.app.get('/sign-up')
        assert b'test case' in rv.data

if __name__ == '__main__':
    unittest.main()