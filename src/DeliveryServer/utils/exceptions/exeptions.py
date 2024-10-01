#Except for when username is already used
class UsernameAlreadyExists(Exception):
    def __init__(self, message="This username has already been used!"):
        self.message = message
        super().__init__(self.message)

class NotFound(Exception):
    def __init__(self, message="This entity was not found!"):
        self.message = message
        super().__init__(self.message)