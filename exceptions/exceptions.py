class ServiceException(Exception):
    pass

class RepositoryException(Exception):
    pass

class DatabaseException(RepositoryException):
    pass
