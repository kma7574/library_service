from sqlalchemy.orm import relationship
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


#대여 현황 테이블
class Book_borrow(db.Model):
    __tablename__ = 'book_borrow'

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    borrow_book_id = db.Column(
        db.Integer, db.ForeignKey(Book.id), nullable=False)
    borrow_user_id = db.Column(
        db.Integer, db.ForeignKey(Member.id), nullable=False)
    borrow_date = db.Column(db.TIMESTAMP, server_default=db.func.now(),
                            onupdate=db.func.now())
    borrow_state = db.Column(db.Boolean, nullable=False,
                             default=0)  # 대출현황(반납x: 0, 반납o: 1)
    return_date = db.Column(db.DateTime)

    def __init__(self, borrow_book_id, borrow_user_id):
        self.borrow_book_id = borrow_book_id
        self.borrow_user_id = borrow_user_id


#대여 후 남은 책, 수량 등 현황 테이블
class Book_remain(db.Model):
	__tablename__ = "book_remain"
	
	id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
	remain_book_id = db.Column(db.Integer, db.ForeignKey(Book.id), nullable=False)
	remain_book_count = db.Column(db.Integer, nullable=False, default=5)

	def __init__(self, remain_book_id, remain_book_count):
		self.remain_book_id = remain_book_id
		self.remain_book_count = remain_book_count
		
