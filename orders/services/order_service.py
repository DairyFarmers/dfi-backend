from exceptions.exceptions import (
    RepositoryException,
    ServiceException
)

class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_orders(self):
        try:
            return self.repository.get_all()
        except RepositoryException as e:
            raise ServiceException('Error while retrieving items')

    def add_order(self, data):
        try:
            return self.repository.create(data)
        except RepositoryException as e:
            raise ServiceException('Error while adding item')
        
    def get_order_by_id(self, item_id):
        try:
            return self.repository.get(id=item_id)
        except RepositoryException as e:
            raise ServiceException('Item not found')
        
    def update_order(self, item_id, **kwargs):
        try:
            return self.repository.update(item_id, **kwargs)
        except RepositoryException as e:
            raise ServiceException('Error while updating item')
        
    def delete_order(self, item_id):
        try:
            return self.repository.delete(item_id)
        except RepositoryException as e:
            raise ServiceException('Error while deleting item')