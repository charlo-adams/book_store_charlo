from user import User

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def save(self, user):
        self._connection.execute('INSERT INTO users (username, password) VALUES (%s, %s)', [user.username, user.password])
        return None

    def find_by_username(self, username):
        users = self._connection.execute('SELECT * FROM users WHERE username = %s', [username])
        if len(users) == 0:
            return None

        user_details = users[0]
        return User(user_details["username"], user_details["password"], user_details["id"])