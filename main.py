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
pets_collection = mongo.db.pets

swagger = Swagger(app)

# Routes
# Add a new pet
@app.route("/add_pet", methods=["POST"])
def add_pet():
    """
    Add a new pet
    ---
    tags:
      - Pet
    parameters:
      - name: pet
        in: body
        required: true
        description: The pet details to be added
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the pet
            age:
              type: integer
              description: The age of the pet
            type:
              type: string
              description: The type of pet (e.g., Dog, Cat)
            owner:
              type: string
              description: The owner's name
          required:
            - name
            - age
            - type
            - owner
    responses:
      201:
        description: Pet added successfully
      400:
        description: Missing required parameters
    """
    data = request.json
    name = data.get("name")
    age = data.get("age")
    type = data.get("type")
    owner = data.get("owner")

    if not name or not age or not type or not owner:
        return jsonify({"error": "Name, age, type, and owner are required"}), 400

    pet_id = pets_collection.insert_one({
        "name": name,
        "age": age,
        "type": type,
        "owner": owner
    }).inserted_id

    return jsonify({"message": "Pet added successfully", "pet_id": str(pet_id)}), 201


# Get all pets
@app.route("/get_all_pets", methods=["GET"])
def get_all_pets():
    """
    Get all pets
    ---
    tags:
      - Pet
    responses:
      200:
        description: List of all pets
    """
    pets = pets_collection.find()
    pets_list = [{"_id": str(pet["_id"]), "name": pet["name"], "age": pet["age"], "type": pet["type"], "owner": pet["owner"]} for pet in pets]
    return jsonify(pets_list), 200

@app.route('/update_pet/<pet_id>', methods=['PUT'])
def update_pet(pet_id):
    """
    Update an existing pet
    --- 
    tags:
      - Pet
    parameters:
      - name: pet_id
        in: path
        required: true
        description: The ID of the pet to be updated
        type: string
      - name: pet
        in: body
        required: true
        description: The updated details of the pet
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the pet
            age:
              type: integer
              description: The age of the pet
            type:
              type: string
              description: The type of the pet (e.g., Dog, Cat)
            owner:
              type: string
              description: The owner's name
          required:
            - name
            - age
            - type
            - owner
    responses:
      200:
        description: Pet updated successfully
      400:
        description: Missing required parameters or invalid pet ID
      404:
        description: Pet not found
    """
    data = request.json
    name = data.get("name")
    age = data.get("age")
    type = data.get("type")
    owner = data.get("owner")

    if not name or not age or not type or not owner:
        return jsonify({"error": "Name, age, type, and owner are required"}), 400

    # Update the pet in the collection
    result = pets_collection.update_one(
        {"_id": ObjectId(pet_id)},
        {"$set": {"name": name, "age": age, "type": type, "owner": owner}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Pet not found"}), 404

    return jsonify({"message": "Pet updated successfully"}), 200
# Get pet by ID
@app.route("/get_pet/<string:pet_id>", methods=["GET"])
def get_pet_by_id(pet_id):
    """
    Get a pet by ID
    ---
    tags:
      - Pet
    parameters:
      - name: pet_id
        in: path
        type: string
        required: true
        description: The ID of the pet to retrieve
    responses:
      200:
        description: A single pet
      404:
        description: Pet not found
    """
    pet = pets_collection.find_one({"_id": ObjectId(pet_id)})
    if pet:
        return jsonify({"_id": str(pet["_id"]), "name": pet["name"], "age": pet["age"], "type": pet["type"], "owner": pet["owner"]}), 200
    return jsonify({"error": "Pet not found"}), 404
# Delete pet by ID
@app.route("/delete_pet/<string:pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    """
    Delete a pet
    ---
    tags:
      - Pet
    parameters:
      - name: pet_id
        in: path
        type: string
        required: true
        description: The ID of the pet to delete
    responses:
      200:
        description: Pet deleted successfully
      404:
        description: Pet not found
    """
    result = pets_collection.delete_one({"_id": ObjectId(pet_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Pet not found"}), 404

    return jsonify({"message": "Pet deleted successfully"}), 200

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




if __name__ == '__main__':
    app.run(debug=True)
