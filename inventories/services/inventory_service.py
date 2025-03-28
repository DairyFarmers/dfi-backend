class InventoryService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_items(self):
        return self.repository.get_all()

    def get_item_by_id(self, item_id):
        return self.repository.get_item_by_id(item_id)

    def add_item(self, data):
        return self.repository.create(data)

    def update_item(self, item_id, data):
        item = self.repository.get_item_by_id(item_id)
        if item:
            return self.repository.update_item(item, data)
        return None

    def delete_item(self, item_id):
        item = self.repository.get_item_by_id(item_id)
        if item:
            return self.repository.delete_item(item)
        return None