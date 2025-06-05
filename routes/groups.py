from flask import Blueprint, request, jsonify
from models import Group, User
from database import db

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/', methods=['POST'])
def create_group():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'user_id')):
        return jsonify({'error': 'Missing required fields'}), 400

    if not User.query.get(data['user_id']):
        return jsonify({'error': 'User not found'}), 404

    new_group = Group(name=data['name'], user_id=data['user_id'])
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'message': 'Group created successfully'}), 201

@groups_bp.route('/<int:user_id>', methods=['GET'])
def get_groups(user_id):
    groups = Group.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': g.id, 'name': g.name} for g in groups]), 200

@groups_bp.route('/group/<int:group_id>', methods=['GET'])
def get_group_by_id(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404
    return jsonify({'id': group.id, 'name': group.name, 'user_id': group.user_id}), 200

