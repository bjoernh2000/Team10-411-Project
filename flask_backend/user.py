from flask_login import UserMixin

class User():
    # other columns
    def __init__(self, user_id):
        self.user_id = user_id

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