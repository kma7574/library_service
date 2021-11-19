from operator import add
from flask import redirect, request, render_template, jsonify, Blueprint, session, g, Flask
from models import Book, Book_remain, Member
from db_connect import db
from flask_bcrypt import Bcrypt

book_service = Blueprint('book_service', __name__)
bcrypt = Bcrypt()

@book_service.route('/inventory',  methods=['GET', 'POST'])
def show_list():
    if request.method == 'POST':
        search_word = request.form['searchWord']
        book_list = db.session.query(Book).filter(Book.book_name.like(f'%{search_word}%')).all()
        search_count = len(book_list)
        book_remain_count = db.session.query(Book_remain.remain_book_count).all()
        return render_template('inventory.html', book_list = book_list, search_count = search_count, search_word=search_word, book_remain_count=book_remain_count)
    else:
        book_list = db.session.query(Book).all()
        search_count = len(book_list)
        book_remain_count = db.session.query(Book_remain.remain_book_count).all()
        print(book_remain_count)
        return render_template('inventory.html', book_list = book_list, search_count = search_count, book_remain_count=book_remain_count)


@book_service.route('/inventory/<int:book_id>',  methods=['GET', 'POST'])
def show_detail(book_id):
    book_info = Book.query.filter(Book.id == book_id).first()
    return render_template('detail.html', book_info = book_info, book_id=book_id)