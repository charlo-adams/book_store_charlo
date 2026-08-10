from app import app
from database_connection import DatabaseConnection
from playwright.sync_api import Page

def test_authentication():
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect() 
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    response = client.post('/sessions', data={
        "username": "test",
        "password":
        "1234"
    })

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/books')

def test_authentication_failed():
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect() 
    connection.execute("TRUNCATE TABLE users;")

    response = client.post('/sessions', data={
        "username": "test",
        "password":
        "1234"
    })

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/sessions/new')    


def test_authentication_with_playwright(page: Page):
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect() 
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');") 

    page.goto("http://127.0.0.1:5001/sessions/new")
    page.get_by_placeholder("Username").fill("test")
    page.get_by_placeholder("Password").fill("1234")
    page.get_by_role("button", name="Submit").click()

    assert page.url == "http://127.0.0.1:5001/books"

def test_failed_authentication_with_playwright(page: Page):
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect() 

    page.goto("http://127.0.0.1:5001/sessions/new")
    page.get_by_placeholder("Username").fill("hello")
    page.get_by_placeholder("Password").fill("bye")
    page.get_by_role("button", name="Submit").click()   

    assert page.url == "http://127.0.0.1:5001/sessions/new"
