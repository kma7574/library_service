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
    print('----------------------------------------------------------')
    print(user_id) # 1 잘출력하고있음
    print(type(user_id)) # integer
    print('----------------------------------------------------------')
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
        # id = db.session.query(Member.id).filter(Member.id == user_id).first()
        print('########################################')
        print(id)
        print('########################################')
        record = Book_borrow(book_id, user_id)
        db.session.add(record)
        db.session.commit()
        return jsonify({"result": "ok"})




def id_check():
    user_id = request.form['user_id']
    id_overlap = Member.query.filter(Member.user_id == user_id).first()
    if id_overlap is not None:  # id가 중복
        return jsonify({"result": "overlap"})
    else:
        return jsonify({"result": "ok"})