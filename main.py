from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from flasgger import Swagger
from bson.objectid import ObjectId  # For MongoDB ObjectId

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://pythonflask:pythonflask@cluster0.pln10.mongodb.net/mydatabase"
mongo = PyMongo(app)
db = mongo.db

users_collection = db.users
books_collection = db.books

swagger = Swagger(app)

# Routes

# Users Routes
@app.route('/get_users', methods=['GET'])
def get_users():
    """
    Get all users
    --- 
    tags:
      - User
    responses:
      200:
        description: List of all users
    """
    users = users_collection.find()
    users_list = [{"_id": str(user["_id"]), "name": user["name"], "age": user["age"], "school": user["school"]} for user in users]
    return jsonify(users_list), 200

@app.route('/get_user/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Get a user by ID
    --- 
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The ID of the user to retrieve
    responses:
      200:
        description: A single user
      404:
        description: User not found
    """
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return jsonify({"_id": str(user["_id"]), "name": user["name"], "age": user["age"], "school": user["school"]}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/add_user', methods=['POST'])
def add_user():
    """
    Add a new user
    --- 
    tags:
      - User
    parameters:
      - name: user
        in: body
        required: true
        description: The user details to be added
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the user
            age:
              type: integer
              description: The age of the user
            school:
              type: string
              description: The school of the user
          required:
            - name
            - age
            - school
    responses:
      201:
        description: User added successfully
      400:
        description: Missing required parameters
    """
    data = request.json
    name = data.get("name")
    age = data.get("age")
    school = data.get("school")

    if not name or not age or not school:
        return jsonify({"error": "Name, age, and school are required"}), 400

    user_id = users_collection.insert_one({"name": name, "age": age, "school": school}).inserted_id
    return jsonify({"message": "User added", "user_id": str(user_id)}), 201

@app.route('/update_user/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user
    --- 
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        required: true
        description: The ID of the user to be updated
        type: string
      - name: user
        in: body
        required: true
        description: The updated details of the user
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the user
            age:
              type: integer
              description: The age of the user
            school:
              type: string
              description: The school of the user
          required:
            - name
            - age
            - school
    responses:
      200:
        description: User updated successfully
      400:
        description: Missing required parameters or invalid user ID
      404:
        description: User not found
    """
    data = request.json
    name = data.get("name")
    age = data.get("age")
    school = data.get("school")

    if not name or not age or not school:
        return jsonify({"error": "Name, age, and school are required"}), 400

    # Update the user in the collection
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"name": name, "age": age, "school": school}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User updated successfully"}), 200


@app.route('/delete_user/<string:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """
    Delete a user by ID
    --- 
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The ID of the user to delete
    responses:
      200:
        description: User deleted successfully
      404:
        description: User not found
    """
    result = users_collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200


# Book Routes
@app.route('/get_books', methods=['GET'])
def get_books():
    """
    Get all books
    --- 
    tags:
      - Book
    responses:
      200:
        description: List of all books
    """
    books = books_collection.find()
    books_list = [{"_id": str(book["_id"]), "title": book["title"], "author": book["author"], "year": book["year"]} for book in books]
    return jsonify(books_list), 200

@app.route('/get_book/<string:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """
    Get a book by ID
    --- 
    tags:
      - Book
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: The ID of the book to retrieve
    responses:
      200:
        description: A single book
      404:
        description: Book not found
    """
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    if book:
        return jsonify({"_id": str(book["_id"]), "title": book["title"], "author": book["author"], "year": book["year"]}), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/add_book', methods=['POST'])
def add_book():
    """
    Add a new book
    --- 
    tags:
      - Book
    parameters:
      - name: book
        in: body
        required: true
        description: The book details to be added
        schema:
          type: object
          properties:
            title:
              type: string
              description: The title of the book
            author:
              type: string
              description: The author of the book
            year:
              type: integer
              description: The publication year of the book
          required:
            - title
            - author
            - year
    responses:
      201:
        description: Book added successfully
      400:
        description: Missing required parameters
    """
    data = request.json
    title = data.get("title")
    author = data.get("author")
    year = data.get("year")

    if not title or not author or not year:
        return jsonify({"error": "Title, author, and year are required"}), 400

    book_id = books_collection.insert_one({"title": title, "author": author, "year": year}).inserted_id
    return jsonify({"message": "Book added", "book_id": str(book_id)}), 201
@app.route('/update_book/<book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Update an existing book
    --- 
    tags:
      - Book
    parameters:
      - name: book_id
        in: path
        required: true
        description: The ID of the book to be updated
        type: string
      - name: book
        in: body
        required: true
        description: The updated details of the book
        schema:
          type: object
          properties:
            title:
              type: string
              description: The title of the book
            author:
              type: string
              description: The author of the book
            year:
              type: integer
              description: The publication year of the book
          required:
            - title
            - author
            - year
    responses:
      200:
        description: Book updated successfully
      400:
        description: Missing required parameters or invalid book ID
      404:
        description: Book not found
    """
    data = request.json
    title = data.get("title")
    author = data.get("author")
    year = data.get("year")

    if not title or not author or not year:
        return jsonify({"error": "Title, author, and year are required"}), 400

    # Update the book in the collection
    result = books_collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": {"title": title, "author": author, "year": year}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"message": "Book updated successfully"}), 200


@app.route('/delete_book/<string:book_id>', methods=['DELETE'])
def delete_book_by_id(book_id):
    """
    Delete a book by ID
    --- 
    tags:
      - Book
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: The ID of the book to delete
    responses:
      200:
        description: Book deleted successfully
      404:
        description: Book not found
    """
    result = books_collection.delete_one({"_id": ObjectId(book_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"message": "Book deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
