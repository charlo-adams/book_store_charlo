class Book:
    def __init__(self, title, author, id = None):
        self.id = id
        self.title = title
        self.author = author


    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Book({self.id}, {self.title}, {self.author})"