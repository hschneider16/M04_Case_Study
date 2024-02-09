# application.py
# by Hunter Schneider
# A database API for books. User can post, get, put, and delete.
# last modified 2/8/2024

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))

    def __init__(self, book_name, author, publisher):
        self.book_name = book_name
        self.author = author
        self.publisher = publisher
        
@app.route('/')
def index():
    return 'Hello!'

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    results = []
    for book in books:
        book_data = {
            'id': book.id,
            'book_name': book.book_name,
            'author': book.author,
            'publisher': book.publisher
        }
        results.append(book_data)
    return jsonify(results)


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        book_data = {
            'id': book.id,
            'book_name': book.book_name,
            'author': book.author,
            'publisher': book.publisher
        }
        return jsonify(book_data)
    return jsonify({'message': 'Book not found'}), 404


@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    book = Book(book_name=data['book_name'], author=data['author'], publisher=data['publisher'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book:
        data = request.get_json()
        book.book_name = data['book_name']
        book.author = data['author']
        book.publisher = data['publisher']
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'})
    return jsonify({'message': 'Book not found'}), 404


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    return jsonify({'message': 'Book not found'}), 404


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
