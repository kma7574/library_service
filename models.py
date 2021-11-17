from db_connect import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    book_name = db.Column(db.String(32), nullable = False)
    publisher = db.Column(db.String(32), nullable = False)
    author = db.Column(db.String(16), nullable = False)
    publication_date = db.Column(db.String(32), nullable = False)
    pages = db.Column(db.Integer, nullable = False)
    isbn = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(800), nullable = False)
    link = db.Column(db.String(512), nullable = False)
    path = db.Column(db.String(256))


class Member(db.Model):
    __tablename__ = 'member'
    
    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    user_id = db.Column(db.String(20),nullable=False, unique = True)
    user_pw = db.Column(db.String(100),nullable=False)
    name = db.Column(db.String(20),nullable=False)
    gender = db.Column(db.String(1),nullable=False)
    phone_number = db.Column(db.String(20),nullable=False)
    address = db.Column(db.String(500),nullable=False)
    join_date = db.Column(db.TIMESTAMP, server_default=db.func.now(),
                  onupdate=db.func.now())

    def __init__(self, user_id, user_pw, name, gender, phone_number, address):
        self.user_id = user_id
        self.user_pw = user_pw
        self.name = name
        self.gender = gender
        self.phone_number = phone_number
        self.address = address