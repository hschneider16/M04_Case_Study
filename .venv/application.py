# application.py
# by Hunter Schneider
# A database API for books which has information about the title, author, and publisher. User can post, get, and delete.
# last modified 2/8/2024

from flask import Flask, jsonify, request

app = Flask(__name__)

books = []

# get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# get a book (by id)
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({'message': 'Book not found'}), 404

# post a book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    book = {
        'id': len(books) + 1,
        'book_name': data['book_name'],
        'author': data['author'],
        'publisher': data['publisher']
    }
    books.append(book)
    return jsonify(book), 201

# delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        books.remove(book)
        return jsonify({'message': 'Book deleted'})
    return jsonify({'message': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)