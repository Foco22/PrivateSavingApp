
class BaseCustomException(Exception):
    def __str__(self):
        return self.__class__.__name__

class UserDoesNotExist(BaseCustomException):
    pass
    
class UserWithGroupAlreadyExists(BaseCustomException):
    pass

class GroupDoesNotExist(BaseCustomException):
    pass

class PlanDoesNotExist(BaseCustomException):
    pass

class SubscriptionDoesNotExist(BaseCustomException):
    pass
