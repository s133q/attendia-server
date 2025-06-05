from flask import Blueprint, jsonify
from models import Group, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/users/<int:user_id>/groups', methods=['GET'])
def get_user_groups(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    groups = Group.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": g.id, "name": g.name} for g in groups])

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')  # optional

    if username:
        # перевірка на унікальність логіна
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Username already taken'}), 409
        user.username = username

    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        user.password_hash = generate_password_hash(password)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200
