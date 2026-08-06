import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

def test_get_books_returns_a_200():
    client = app.test_client()

    response = client.get("/books")
    assert response.status_code == 200





def test_to_get_authors_returns_a_hard_coded_list_of_authors():
    client = app.test_client()
    response = client.get("/authors")

    assert response.json == [
      {
        "title": "The Gruffalo",
        "author": "Julia Donaldson"
      },
      {
        "title": "Ada Twist, Scientist",
        "author": "Andrea Beaty"
      },
      {
        "title": "The Girl Who Drank the Moon",
        "author": "Kelly Barnhill"
      },
      {
        "title": "Dragons in a Bag",
        "author": "Zetta Elliott"
      }
    ]