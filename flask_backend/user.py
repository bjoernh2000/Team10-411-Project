from mongoengine import Document, UUIDField

class User(Document):
    session_id = UUIDField(binary=False, required=True)
    user_id = UUIDField(binary=False, required=True)

    # other columns
    @property
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