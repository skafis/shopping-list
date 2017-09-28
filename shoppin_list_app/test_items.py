import unittest
from store import Store

class ItemListTestcase(unittest.TestCase):
    def setUp(self):
        self.item = Store()
    
    def test_add_item(self):
        self.item.add_list_item('item 1')
        print('items')
        self.assertIn('item 1', self.item.item_list)
    
    def test_update_item(self):
        pass
    
    def test_delete_item(self):
        pass


if __name__ == '__main__':
    unittest.main()