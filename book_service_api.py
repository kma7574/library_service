from operator import add
from flask import redirect, request, render_template, jsonify, Blueprint, session, g, Flask
from models import Book, Book_borrow, Book_remain, Member
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
        return render_template('inventory.html', book_list = book_list, search_count = search_count, book_remain_count=book_remain_count)


@book_service.route('/inventory/<int:book_id>',  methods=['GET', 'POST'])
def show_detail(book_id):
    book_info = Book.query.filter(Book.id == book_id).first()
    return render_template('detail.html', book_info = book_info, book_id=book_id)


@book_service.route('/borrow_check', methods=['POST'])
def borrow_check():
    book_id = request.form['book_id']
    user_id = session.get('login') # 로그인값은 불러오는것같음
    if user_id is None:
        return jsonify({"result": "need_login"})
    # 잔여수량 테이블에 남은 권수 확인하고 대출처리한다음 수량 -1 업데이트
    remain_count = db.session.query(Book_remain.remain_book_count).filter(Book_remain.remain_book_id == book_id).first()
    # print(remain_count)
    if remain_count[0] == 0: #대출이 불가능한 경우
        return jsonify({"result": "not_remain"})
    else:
        update_book = Book_remain.query.filter(Book_remain.remain_book_id == book_id).first()
        update_book.remain_book_count = remain_count[0] -1
        db.session.commit()
        # 대출테이블에 추가
        record = Book_borrow(book_id, user_id)
        db.session.add(record)
        db.session.commit()
        return jsonify({"result": "ok"})


@book_service.route('/myborrow/<int:user_id>', methods=['GET'])
def myborrow(user_id):
    myborrow_list = Book_borrow.query.filter(Book_borrow.borrow_user_id == user_id).all()
    print('---------------------------------------------------------------------')
    print(myborrow_list[2].borrow_book_id)
    print(len(myborrow_list))
    print('---------------------------------------------------------------------')
    if len(myborrow_list) == 0: #로그인한유저가 현재 대출한 이력이 없음
        return render_template('myborrow.html', myborrow_list = myborrow_list)
    else: #로그인한 유저가 한권이상 대출한 이력이 있다.
        book_name = db.session.query(Book.book_name).join(Book_borrow, Book_borrow.borrow_book_id == Book.id).all()
        book_title = []
        for i in range(len(myborrow_list)):
            print(book_name[i].book_name)
            book_title.append(book_name[i].book_name)
        name = db.session.query(Member.name).join(Book_borrow, Book_borrow.borrow_user_id == Member.id).all()
        return render_template('myborrow.html', myborrow_list = myborrow_list, book_name=book_title, name=name[0][0])