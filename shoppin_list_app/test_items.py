import unittest
from store import Store

class ItemListTestcase(unittest.TestCase):
    def setUp(self):
        self.item = Store()
    
    def test_add_item(self):
        '''
        checks if can add an item to list
        '''
        self.item.add_list_item('item 1')
        self.assertIn('item 1', self.item.item_list)
    
    def test_update_item(self):
        '''
        checks if the item can update
        '''
        pass
    
    def test_delete_item(self):
        '''
        check if the items can be deleted
        '''
        pass


if __name__ == '__main__':
    unittest.main()