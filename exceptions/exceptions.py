class ServiceException(Exception):
    pass

class RepositoryException(Exception):
    pass

class DatabaseException(RepositoryException):
    pass

class InvalidDataException(ServiceException):
    pass

class InvalidCredentialsException(ServiceException):
    pass


