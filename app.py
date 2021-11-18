from flask import *
import pymysql
from db_connect import db #sqlalchemy객체 가져옴
from user_api import user
from book_service_api import book_service

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(book_service)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:yourpass@127.0.0.1:3306/elice_library"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = 'dfjlkwjlkc'

db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)