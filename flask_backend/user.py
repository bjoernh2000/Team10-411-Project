from flask_login import UserMixin

class User():
    # other columns
    def __init__(self, user_id, authorization_header):
        self.user_id = user_id
        self.authorization_header = authorization_header

    def get_id(self):
        return self.user_id

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False