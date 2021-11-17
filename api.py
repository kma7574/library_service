from operator import add
from flask import redirect, request, render_template, jsonify, Blueprint, session, g, Flask
from models import Book, Member
from db_connect import db
from flask_bcrypt import Bcrypt

board = Blueprint('board', __name__)
bcrypt = Bcrypt()

@board.route('/')
def home():
    book_list = Book.query.all()
    return render_template('index.html', book_list = book_list)
    
@board.route('/post', methods=['GET'])
def post():
    return render_template('index.html')

@board.route('/join', methods=['GET', 'POST'])
def join():
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


@board.route('/login', methods=['GET', 'POST'])
def login():
   return render_template('login.html')
