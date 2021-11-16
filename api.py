from flask import redirect, request, render_template, jsonify, Blueprint, session, g, Flask
from models import Member
from db_connect import db
# from flask_bcrypt import Bcrypt

board = Blueprint('board', __name__)
# bcrypt = Bcrypt()

@board.route('/')
def home():
    return render_template('index.html')
    
@board.route('/post', methods=['GET'])
def post():
    return render_template('index.html')

@board.route('/join', methods=['GET', 'POST'])
def join():
    member_list = Member.query
    cnt = member_list.count()
    print(f"count:{cnt}")
    return render_template('tmp.html')
# @board.route('/join', methods=['GET', 'POST'])
# def join():
    # user_id = 'lorem'
    # user_pw = 'ipsum'
    # # pw_hash = bcrypt.generate_password_hash(user_pw) #비밀번호를 임의의 해쉬값으로 암호화

    # Member.query.delete()

    # user = Member(user_id,user_pw,"로렘", "0", "010-1234-5678", "서울특별시")
    # user1 = Member("aaaa","1111", "AAAA", "1", "010-8765-4321", "인천광역시")
    # db.session.add(user)
    # db.session.add(user1)
    # db.session.commit()
    # member_list = Member.query
    # cnt = member_list.count()
    # check = db.session.query(Member.id).first()
    # my_fruit = '수박'
    # print(my_fruit)
    # print(check[0])
    # print(f"count:{cnt}")
    # return render_template('tmp.html')


# @board.route('/')
# def hello():
#    return render_template('address_popup.html')
#     # return "hello world"