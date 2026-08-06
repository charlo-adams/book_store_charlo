from database_connection import DatabaseConnection
from flask import Flask, render_template, request, redirect
from book_repository import BookRepository
from book import  Book
from user_repository import UserRepository
from user import User

# instantiate a flask app object
app = Flask(__name__)


# declare a route that listens for a GET request
# and a method to execute when the request comes in
@app.route('/hello', methods=['GET'])
def hello():
    return "hello to you to brotha!"

@app.route('/bye', methods=['GET'])
def byebye():
    return "see ya later alligator"


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/team", methods=['GET'])
def get_team():
    team = ["Dorothy", "Rose", "Blanche", "Sophia"]
    return render_template("team.html", team=team)


@app.route('/books', methods=['GET'])
def get_all_books():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    books = book_repository.all()
    print(books)
    return render_template("books.html", books=books)

@app.route('/books', methods=['POST'])
def create_book():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    book_details = request.form
    new_book = Book(title=book_details["title"], author=book_details["author"])
    book_repository.create(new_book)
    return redirect("/books")

@app.route('/users/new', methods=['GET'])
def get_sign_up_form():
    return render_template("signup_form.html")

@app.route('/users', methods=['POST'])
def save_user():
    connection = DatabaseConnection()
    connection.connect()
    user_repo = UserRepository(connection)
    user_details = request.form
    new_user = User(username=user_details["username"], password=user_details["password"])
    user_repo.save(new_user)
    return redirect("/books")



    

@app.route('/authors', methods=['GET'])
def authors_list():
    authors = [
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
    return authors
# make the server run when ptrhon app.py is put in terminal
# on port 5001 
# and use debug mode so that changing code restarts the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)