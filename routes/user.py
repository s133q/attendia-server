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
