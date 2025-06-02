from flask import Blueprint, request, jsonify
from models import Student

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
def get_students():
    group_id = request.args.get('group_id')
    if not group_id:
        return {'error': 'Missing group_id'}, 400

    students = Student.query.filter_by(group_id=group_id).all()
    return jsonify([
        {'id': s.id, 'first_name': s.first_name, 'last_name': s.last_name}
        for s in students
    ])

