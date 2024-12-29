from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuring the Flask app to connect to the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yochel@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'SQLALCHEMY_TRACK_MODIFICATIONS'

db = SQLAlchemy(app)

# Database model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'second_name': self.second_name
        }

# Create
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(id=data['id'], first_name=data['first_name'], second_name=data['second_name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user": new_user.to_dict()}), 201

# Read all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Read single user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

# Update
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.first_name = data.get('first_name', user.first_name)
    user.second_name = data.get('second_name', user.second_name)
    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": user.to_dict()})

# Delete
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

@app.errorhandler(500)
def not_found_error(error):
    return jsonify({"message": "Not valid data"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Обязательно создайте все таблицы перед запуском приложения
    app.run(host="0.0.0.0", port=5000)
