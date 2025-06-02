from flask import Blueprint, request, jsonify
from models import Lesson, Group
from database import db

lessons_bp = Blueprint('lessons', __name__)

@lessons_bp.route('/', methods=['POST'])
def create_lesson():
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'group_id')):
        return jsonify({'error': 'Missing required fields'}), 400

    if not Group.query.get(data['group_id']):
        return jsonify({'error': 'Group not found'}), 404

    new_lesson = Lesson(title=data['title'], group_id=data['group_id'])
    db.session.add(new_lesson)
    db.session.commit()
    return jsonify({'message': 'Lesson created successfully'}), 201

@lessons_bp.route('/group/<int:group_id>', methods=['GET'])
def get_lessons(group_id):
    lessons = Lesson.query.filter_by(group_id=group_id).all()
    return jsonify([{'id': l.id, 'title': l.title} for l in lessons]), 200
