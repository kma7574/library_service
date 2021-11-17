from flask import *
import pymysql
from db_connect import db #sqlalchemy객체 가져옴
from api import board

app = Flask(__name__)
app.register_blueprint(board)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:yourpass@127.0.0.1:3306/elice_library"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)