from flask import Blueprint, request, jsonify
from models import Group, User, Student, Lesson, LessonDay
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

@groups_bp.route('/<int:group_id>', methods=['GET'])
def get_group_by_id(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404
    return jsonify({'id': group.id, 'name': group.name, 'user_id': group.user_id}), 200

@groups_bp.route('/<int:group_id>', methods=['PUT'])
def update_group_name(group_id):
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing group name'}), 400

    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    group.name = data['name']
    try:
        db.session.commit()
        return jsonify({'message': 'Group name updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update group name'}), 500

@groups_bp.route('/full/<int:group_id>', methods=['GET'])
def get_full_group_data(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    students = Student.query.filter_by(group_id=group_id).order_by(Student.last_name).all()
    student_data = [{'id': s.id, 'first_name': s.first_name, 'last_name': s.last_name} for s in students]

    lessons = Lesson.query.filter_by(group_id=group_id).all()
    lesson_data = []
    for lesson in lessons:
        lesson_days = LessonDay.query.filter_by(lesson_id=lesson.id).all()
        days = [ld.day_of_week for ld in lesson_days]
        lesson_data.append({
            'id': lesson.id,
            'title': lesson.title,
            'days': days
        })

    return jsonify({
        'group': {'id': group.id, 'name': group.name},
        'students': student_data,
        'lessons': lesson_data
    }), 200
