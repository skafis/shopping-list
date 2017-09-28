'''
This is the method files for the Shopping list class
'''
class Store():
    '''
    Mehods for shopping list mannipulation
    '''
    def __init__(self):
        self.shopping_list = {}
        self.last_slist_id = 0
        self.item_list = []

    def add_slist(self, slist):
        ''''''
        self.last_slist_id += 1
        self.shopping_list[self.last_slist_id] = slist
        print(type(slist))
        slist._id = self.last_slist_id

    def update_slist(self, slist):
        self.shopping_list[slist._id] = slist

    def delete_slist(self, slist_id):
        del self.shopping_list[slist_id]

    def get_slist(self, slist_id):
        return self.shopping_list[slist_id]

    def get_all_slist(self):
        return self.shopping_list

    def add_list_item(self, item):
        self.item_list.append(item)