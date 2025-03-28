from exceptions.exceptions import (
    RepositoryException,
    ServiceException
)

class InventoryService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_items(self):
        try:
            return self.repository.get_all()
        except RepositoryException as e:
            raise ServiceException('Error while retrieving items')

    def add_item(self, data):
        try:
            return self.repository.create(data)
        except RepositoryException as e:
            raise ServiceException('Error while adding item')
        
    def get_item_by_id(self, item_id):
        try:
            return self.repository.get(id=item_id)
        except RepositoryException as e:
            raise ServiceException('Item not found')
        
    def update_item(self, item_id, **kwargs):
        try:
            return self.repository.update(item_id, **kwargs)
        except RepositoryException as e:
            raise ServiceException('Error while updating item')
        
    def delete_item(self, item_id):
        try:
            return self.repository.delete(item_id)
        except RepositoryException as e:
            raise ServiceException('Error while deleting item')