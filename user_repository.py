from user import User

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def save(self, user):
        self._connection.execute('INSERT INTO users (username, password) VALUES (%s, %s)', [user.username, user.password])
        return None