from app import app
from playwright.sync_api import Page, expect
from database_connection import DatabaseConnection

#def test_list_of_books(page: Page):
#    connection = DatabaseConnection()
#    connection.connect()
#    connection.seed("./seeds/books.sql")
#    page.goto("http://127.0.0.1:5001/books")


#    books = page.locator("li")

#    expected_books = [
#    'The Gruffalo, by Julia Donaldson',
#    'Ada Twist, Scientist, by Andrea Beaty',
#    'The Girl Who Drank the Moon, by Kelly Barnhill',
#    'Dragons in a Bag, by Zetta Elliott'
#   ]

#    actual_books = books.all_inner_texts()

#    assert actual_books == expected_books

def test_title_is_present(page: Page):
    page.goto("http://127.0.0.1:5001/books")

    title = page.locator("h1")
    expect(title).to_have_text("My Books")

def test_form_interaction(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    page.goto("http://127.0.0.1:5001/sessions/new")
    page.get_by_placeholder("Username").fill("test")
    page.get_by_placeholder("Password").fill("1234")
    page.get_by_role("button", name="Submit").click()

    page.goto("http://127.0.0.1:5001/books")
    page.get_by_placeholder("Title").fill("The Chroicles of Geronimo (the cat)")
    page.get_by_placeholder("Author").fill("Geronimo")
    page.get_by_role("button", name="Submit").click()
    page.wait_for_load_state("networkidle")

    print(page.url)
    print(page.locator("li").all_inner_texts())

    books = page.locator("li")
    new_book = books.all_inner_texts()[-1]

    assert new_book == "The Chroicles of Geronimo (the cat), by Geronimo"


def test_unauthenticated_user_trying_to_write_in_new_book(page: Page):
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect() 
    connection.execute("TRUNCATE TABLE users;")


    page.goto("http://127.0.0.1:5001/books")
    page.get_by_placeholder("Title").fill("Death Note")
    page.get_by_placeholder("Author").fill("Tsugumi")
    page.get_by_role("button", name="Submit").click()
    page.wait_for_load_state("networkidle")

    books = page.locator("li")

    assert page.url == "http://127.0.0.1:5001/sessions/new"