from flask import Blueprint, jsonify
from models import Group

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    return jsonify([{'id': g.id, 'name': g.name} for g in groups])

