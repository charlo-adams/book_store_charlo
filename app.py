from database_connection import DatabaseConnection
from flask import Flask, render_template, request, redirect, session
from book_repository import BookRepository
from book import  Book
from user_repository import UserRepository
from user import User
from authenticated import *
from login_required import login_required

# instantiate a flask app object
app = Flask(__name__)

app.secret_key = "some_really_secret_key"


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


# lists all books added to DB
@app.route('/books', methods=['GET'])
def get_all_books():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    books = book_repository.all()
    print(books)
    return render_template("books.html", books=books)



@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    book = book_repository.find(book_id)
    return render_template("one_book.html", book=book)



#render add to books form
@app.route("/add_to_books", methods=['GET'])
def get_add_book_form():
    return render_template("add_book.html")


# add to list of books in the database
@app.route('/add_to_books', methods=['POST'])
@login_required
def create_book():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    book_details = request.form
    new_book = Book(title=book_details["title"], author=book_details["author"])
    book_repository.create(new_book)
    return redirect("/books")


# render signup form
@app.route('/users/new', methods=['GET'])
def get_sign_up_form():
    return render_template("signup_form.html")


# save user and password to user table in DB
@app.route('/users', methods=['POST'])
def save_user():
    connection = DatabaseConnection()
    connection.connect()
    user_repo = UserRepository(connection)
    user_details = request.form
    new_user = User(username=user_details["username"], password=user_details["password"])
    user_repo.save(new_user)
    return redirect("/books")


#renders login form html page by "getting" the login form
@app.route('/sessions/new', methods=['GET'])
def get_login_form():
    return render_template("login_form.html")


#using HTTP method POST to create data
@app.route('/sessions', methods=['POST'])
def verify_login():
    #connects to database (this holds books but also user information such as username/passwords)
    connection = DatabaseConnection()
    connection.connect()
    #connect ot user repository
    user_repo = UserRepository(connection)
    #get the inputted username/password 
    username = request.form["username"]
    password = request.form["password"]
    # using the user repo it finds if the username exsists within the DB
    user = user_repo.find_by_username(username)

    if user and user.password == password:
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/books")
    else:
        return redirect("/sessions/new")
        



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