from datetime import datetime
from operator import add
from flask import redirect, request, render_template, jsonify, Blueprint, session, g, Flask
from models import Book, Book_borrow, Book_remain, Member, Book_review
from db_connect import db
from flask_bcrypt import Bcrypt

book_service = Blueprint('book_service', __name__)
bcrypt = Bcrypt()

@book_service.route('/inventory',  methods=['GET', 'POST'])
def show_list():

    if request.method == 'POST':
        search_word = request.form['searchWord']
        book_list = db.session.query(Book.id, Book.book_name, Book.path, Book_remain.remain_book_count).join(Book, Book_remain.id == Book.id).filter(Book.book_name.like(f'%{search_word}%'))
        search_count = book_list.count()
        page = request.args.get('page', type=int, default=1)  # 페이지
        pagination = book_list.paginate(page, per_page=8)
        return render_template('inventory.html', book_list = book_list, search_count = search_count, search_word=search_word, pagination=pagination)
    else:
        book_list = book_list = db.session.query(Book.id, Book.book_name, Book.path, Book_remain.remain_book_count).join(Book, Book_remain.id == Book.id)
        search_count = book_list.count()
        page = request.args.get('page', type=int, default=1)  # 페이지
        pagination = book_list.paginate(page, per_page=8)
        return render_template('inventory.html', book_list = book_list, search_count = search_count, pagination=pagination)


@book_service.route('/inventory/<int:book_id>',  methods=['GET', 'POST'])
def show_detail(book_id):
    if request.method =='GET':
        book_info = Book.query.filter(Book.id == book_id).first()
        review_data = Book_review.query.filter(Book_review.book_id == book_id).order_by(Book_review.created.desc()).all()
        return render_template('detail.html', book_info = book_info, book_id=book_id, review_data=review_data)
    else:
        content = request.form['content']
        score = request.form['score']
        id = db.session.query(Member.id).filter(Member.user_id == g.user.user_id).first()
        check_review=Book_review.query.filter(Book_review.user_id == id[0], Book_review.book_id == book_id).count()
        if check_review >=1: #사용자가 이미 리뷰를 남겼음
            return jsonify({"result":"already_review"})
        review = Book_review(id[0], book_id, content, score)
        db.session.add(review)
        db.session.commit()
        # 리뷰댓글의 모든평점합 / 리뷰댓글 개수
        
        review_score_sum = db.session.query(db.func.sum(Book_review.score)).first()[0]
        review_count = Book_review.query.count()
        update_rating = Book.query.filter(Book.id == Book_review.book_id).first()
        update_rating.rating = round(review_score_sum/review_count, 1) # 첫째자리에서 반올림
        db.session.commit()
        
        return jsonify({"result":"success"})



@book_service.route('/borrow_check', methods=['POST'])
def borrow_check():
    book_id = request.form['book_id'] #숫자값
    user_id = session.get('login') # 로그인값(숫자값)은 불러오는것같음
    if user_id is None:
        return jsonify({"result": "need_login"})
    '''
    잔여수량 테이블에 남은 권수 확인하고 대출처리한다음 수량 -1 업데이트
    '''
    record = db.session.query(Book_borrow).filter((Book_borrow.borrow_book_id == book_id) & (Book_borrow.borrow_user_id == user_id))
    if record.count() >= 1:
        return jsonify({"result": "already_borrow"})
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


@book_service.route('/<int:user_id>', methods=['GET', 'POST'])
def myborrow(user_id):
    # print('?????????????????????????????????????????????????????')
    name = db.session.query(Member.name).filter(Member.id == user_id).first()
    myborrow_list = db.session.query(Book_borrow.borrow_state, Book_borrow.borrow_date, Book_borrow.return_date, Book_borrow.borrow_book_id, Book_borrow.id, Book.book_name).join(Book, Book_borrow.borrow_book_id == Book.id).filter(Book_borrow.borrow_user_id == user_id)
    book_cnt = myborrow_list.count()
    if book_cnt == 0:  # 로그인한유저가 현재 대출한 이력이 없음
        return render_template('myborrow.html', myborrow_list=myborrow_list,  name=name[0], cnt=0, borrow_ing=0)
    else:  # 로그인한 유저가 한권이상 대출한 이력이 있다.
        book_name = db.session.query(Book.book_name).join(Book_borrow, Book_borrow.borrow_book_id == Book.id).all()
        page = request.args.get('page', type=int, default=1)  # 페이지
        pagination = myborrow_list.paginate(page, per_page=10)
        book_title = []
        borrow_ing = 0 # 현재 대출중인 책 수
        for i in range(book_cnt):
            book_title.append(book_name[i].book_name)
            if myborrow_list[i].borrow_state == 0:
                borrow_ing += 1
        return render_template('myborrow.html', myborrow_list=myborrow_list, book_name=book_title, name=name[0], cnt=book_cnt, borrow_ing=borrow_ing, pagination=pagination)



@book_service.route('/return_check', methods=['POST', 'GET'])
def return_check():
    if request.method == 'POST':
        idx = request.form['idx']
        user_id = session.get('login') # 로그인값은 불러오는것같음
        if user_id is None:
            return jsonify({"result": "need_login"})
        # 반납처리로직
        # 반납하기 버튼을누르면 해당 아이디에 해당하는 책의 남은 수량카운트를 +1 해준다, borrow_state값을 0에서 1로 바꿔준다.
        # remain_count = db.session.query(Book_remain.remain_book_count).filter(Book_borrow.id == book_id).first()
        borrow = db.session.query(Book_borrow).filter(Book_borrow.borrow_user_id == user_id).offset(int(idx)-1).first()
        print(user_id)
        print(borrow)
        remain_count = db.session.query(Book_remain).filter(Book_remain.remain_book_id == Book_borrow.borrow_book_id).all()
        if remain_count[0] == 5: #책의 최대수량은 5인데 반납하기전 권수가 5권이면 뭔가 오류가 생긴것(각 책의 최대수량은 추후 변경 가능)
            return jsonify({"result": "unknown_error"})
        else:
            update_book = Book_remain.query.filter(Book_remain.remain_book_id == borrow.borrow_book_id).first()
            update_book.remain_book_count += 1
            db.session.commit()
            # 대여현황테이블의 반납상태 업데이트
            update_state = Book_borrow.query.filter((Book_borrow.borrow_book_id == borrow.borrow_book_id) & (Book_borrow.borrow_state == False)).first()
            update_state.borrow_state = True
            now = datetime.now()
            update_state.return_date = now
            db.session.commit()
            return jsonify({"result": "ok"})
    else:
        return redirect('/')


@book_service.route('/inventory/<int:id>', methods=['DELETE'])
def delete_content(id):
    id = request.form['id']
    data = Book_review.query.filter(Book_review.id == id).first()
    if data is not None:
        db.session.delete(data)
        db.session.commit()
        review_score_sum = db.session.query(db.func.sum(Book_review.score)).first()[0]
        review_count = Book_review.query.count()
        update_rating = Book.query.filter(Book.id == Book_review.book_id).first()
        update_rating.rating = round(review_score_sum/review_count, 1) # 첫째자리에서 반올림
        db.session.commit()
        return jsonify({"result": "success"})
    else:
        return jsonify({"result": "fail"})


@book_service.route("/inventory/<int:id>", methods=["PATCH"])
def update_post(id):
    id = request.form['id']
    content = request.form['content']
    author = Member.query.filter(Member.id == session['login']).first()
    data = Book_review.query.filter(Book_review.id == id).first()
    data.content = content
    db.session.commit()
    review_score_sum = db.session.query(db.func.sum(Book_review.score)).first()[0]
    review_count = Book_review.query.count()
    update_rating = Book.query.filter(Book.id == Book_review.book_id).first()
    update_rating.rating = round(review_score_sum/review_count, 1) # 첫째자리에서 반올림
    db.session.commit()
    return jsonify({"result":"success"})

@book_service.route('/temp')
def _list():
    return render_template('tmp.html')