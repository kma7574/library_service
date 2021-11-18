from operator import add
from flask import redirect, request, render_template, jsonify, Blueprint, session, g, Flask
from models import Book, Member
from db_connect import db
from flask_bcrypt import Bcrypt

user = Blueprint('user', __name__)
bcrypt = Bcrypt()


@user.before_app_request #모든 요청전에 실행
def load_logged_member():#로그인 체크 모듈
    user_id = session.get('login') #세션값 가져옴
    if user_id is None:
        g.user = None
    else:
         g.user = Member.query.filter(Member.id == user_id).first()

@user.route('/')
def home():
    book_list = Book.query.all()
    return render_template('index.html', book_list = book_list)
    
@user.route('/post', methods=['GET'])
def post():
    return render_template('index.html')

@user.route('/join', methods=['GET', 'POST'])
def join():
    if session.get('login') is None:
        if request.method == 'POST':
            user_id = request.form['user_id']
            user_pw = request.form['user_pw']
            pw_hash = bcrypt.generate_password_hash(user_pw) #비밀번호를 임의의 해쉬값으로 암호화
            name = request.form['name']
            gender = request.form['gender']
            phone_number = request.form['phone_number']
            address = request.form['address']
            
            user = Member(user_id, pw_hash, name, gender, phone_number, address)
            db.session.add(user)
            db.session.commit()
            return jsonify({"result":"success"})
        else:
            return render_template('join.html')
    else: #로그인한 상태
        redirect('/')


@user.route('/id_check', methods=['GET', 'POST'])
def id_check():
    user_id = request.form['user_id']
    id_overlap = Member.query.filter(Member.user_id == user_id).first()
    if id_overlap is not None:  # id가 중복
        return jsonify({"result": "overlap"})
    else:
        return jsonify({"result": "ok"})


@user.route('/login', methods=['POST','GET'])
def login():
    if session.get('login') is None:
        if request.method == 'POST':
            user_id = request.form['user_id']
            user_pw = request.form['user_pw']
            user = Member.query.filter(Member.user_id == user_id).first()
            
            if user is not None:#입력한 아이디가 db에 존재한다면
                if bcrypt.check_password_hash(user.user_pw, user_pw):
                    session['login'] = user.id #'login'으로 user_id를 세션에 저장
                    print("wow")
                    return jsonify({"result" : "success"})
                else:
                    return jsonify({"result" : "pw_fail"})
            else:
                return jsonify({"result" : "id_fail"})
        else:
            return render_template('login.html')
    else:
        return redirect('/')


@user.route('/logout')
def logout():
    session['login'] = None
    return redirect('/')

@user.route('/tmp', methods=['GET'])
def tmp():
    book_list = Book.query.all()
    return render_template('tmp.html', book_list = book_list)

