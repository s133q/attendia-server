from flask import Blueprint, request, jsonify
from models import Student, Group
from database import db

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or not all(k in data for k in ('first_name', 'last_name', 'group_id')):
        return jsonify({'error': 'Missing required fields'}), 400

    if not Group.query.get(data['group_id']):
        return jsonify({'error': 'Group not found'}), 404

    new_student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        group_id=data['group_id']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully'}), 201

@students_bp.route('/group/<int:group_id>', methods=['GET'])
def get_students(group_id):
    students = Student.query.filter_by(group_id=group_id).all()
    return jsonify([{'id': s.id, 'first_name': s.first_name, 'last_name': s.last_name} for s in students]), 200
