from abc import ABC, abstractmethod

class BaseRepositoryInterface(ABC):
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def create(self, data):
        pass
    
    @abstractmethod
    def update(self, entity, data):
        pass
    
    @abstractmethod
    def delete(self, entity):
        pass