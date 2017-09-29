import unittest
from store import Store

class ShoppingListTestcase(unittest.TestCase):
    '''
    This class is responsible for testing the list use cases
    '''

    def setUp(self):
        self.list_db = Store()

    def test_add_items_to_list(self):
        '''
        the test checks if data can be added to items list
        '''
        self.list_db.add_slist('new list')
        check_db = self.list_db.get_all_slist()
        self.assertIn('new list', self.list_db.get_all_slist())

if __name__ == '__main__':
    unittest.main()
