from operator import add
from flask import redirect, request, render_template, jsonify, Blueprint, session, g, Flask
from models import Book, Member
from db_connect import db
from flask_bcrypt import Bcrypt

book_service = Blueprint('book_service', __name__)
bcrypt = Bcrypt()

@book_service.route('/list',  methods=['GET', 'POST'])
def show_list():
    book_list = Book.query.all()
    return render_template('detail.html', book_list = book_list)