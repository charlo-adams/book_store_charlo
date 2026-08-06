import sys
import os 

from app import app
from database_connection import DatabaseConnection

def test_create_user_is_created_and_saved():
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect()

    connection.execute("TRUNCATE TABLE users;")
    # send request
    response = client.post('/users', data={
        'username': 'testuser',
        'password': 'password1234'
    })

    assert response.status_code == 302

    result = connection.execute("SELECT * FROM users WHERE username = 'testuser'")

    assert result[0]['username'] == 'testuser' 