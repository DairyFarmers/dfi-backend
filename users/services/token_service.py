from exceptions.exceptions import InvalidDataException

class TokenService:
    def __init__(self, token_generator):
        self.token_generator = token_generator
        
    def generate_token(self, user):
        return self.token_generator.make_token(user)
    
    def validate_token(self, user, token):
        if not self.token_generator.check_token(user, token):
            raise InvalidDataException('Invalid token')
        return True