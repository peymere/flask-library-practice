#!/usr/bin/env python3

from models import db, Member, Book, Loan
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db, render_as_batch=True)

db.init_app(app)
api = Api(app)

@app.route('/')
def index():
    return '<h1>Library Practice Challenge</h1>'


class Books(Resource):
    def get(self):
        books = [b.to_dict(only=('id','author','title')) for b in Book.query.all()]
        return make_response(
            books,
            200
        )
api.add_resource(Books, '/books')

class BookByID(Resource):
    def get(self, id):
        book = Book.query.get( id )
        if not book:
            return make_response({ 'error': 'Book not found'}, 404)
        return make_response(book.to_dict(), 200)
    
    def delete(self, id):
        book = Book.query.get( id )
        if not book:
            return make_response({'error': 'Book not found'}, 404)
        db.session.delete(book)
        db.session.commit()
        return make_response('', 204)
        
api.add_resource(BookByID, '/books/<int:id>')


class Members(Resource):
    def get(self):
        members = [m.to_dict(only=('id', 'name', 'year_joined')) for m in Member.query.all()]
        return make_response(
            members,
            200
        )
api.add_resource(Members, '/members')

class Loans(Resource):
    def post(self):
        params = request.json
        try:
            loan = Loan(book_id=params['book_id'], member_id=params['member_id'])
        except ValueError as v_error:
            return make_response({'error': [str(v_error)]}, 422)
        db.session.add(loan)
        db.session.commit()
        return make_response(loan.to_dict(), 201)
api.add_resource(Loans, '/loans')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
