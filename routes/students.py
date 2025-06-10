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

    try:
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Student added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add student'}), 500

@students_bp.route('/group/<int:group_id>', methods=['GET'])
def get_students(group_id):
    students = Student.query.filter_by(group_id=group_id).all()
    return jsonify([{'id': s.id, 'first_name': s.first_name, 'last_name': s.last_name} for s in students]), 200

@students_bp.route('/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Студент не знайдений'}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Студента видалено'}), 200

@students_bp.route('/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    if not data or not all(k in data for k in ('first_name', 'last_name')):
        return jsonify({'error': 'Missing required fields'}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    student.first_name = data['first_name']
    student.last_name = data['last_name']

    try:
        db.session.commit()
        return jsonify({'message': 'Student updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update student'}), 500
