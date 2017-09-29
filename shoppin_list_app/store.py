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
        self.user_list = []

    def add_slist(self, slist):
        '''
        Is responsible for adding list
        '''
        self.last_slist_id += 1
        self.shopping_list[self.last_slist_id] = slist
        slist._id = self.last_slist_id

    def update_slist(self, slist):
        '''
        takes in an id and updates list
        '''
        self.shopping_list[slist._id] = slist

    def delete_slist(self, slist_id):
        '''
        Takes in an id and deletes the list
        '''
        del self.shopping_list[slist_id]

    def get_slist(self, slist_id):
        '''
        Takes in a ID and returns the shopping list
        '''
        return self.shopping_list[slist_id]

    def get_all_slist(self):
        '''
        Returns all the shopping list
        '''
        return self.shopping_list

    def add_list_item(self, item):
        '''
        takes in an item
        and adds it to the list
        '''
        self.item_list.append(item)