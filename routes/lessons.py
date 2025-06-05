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

from models import Lesson, Group, User, LessonDay
from datetime import datetime

@lessons_bp.route('/today/<int:user_id>', methods=['GET'])
def get_todays_lessons(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    day_names = ["Понеділок", "Вівторок", "Середа", "Четвер", "П’ятниця", "Субота", "Неділя"]
    today_name = day_names[datetime.today().weekday()]

    lessons = (
        db.session.query(Lesson.id.label("lesson_id"),
                         Group.id.label("group_id"),
                         Group.name.label("group_name"),
                         Lesson.title.label("title"))
        .join(Group, Lesson.group_id == Group.id)
        .join(User, Group.user_id == User.id)
        .join(LessonDay, Lesson.id == LessonDay.lesson_id)
        .filter(User.id == user_id, LessonDay.day_of_week == today_name)
        .all()
    )

    result = [
        {
            "lesson_id": l.lesson_id,
            "group_id": l.group_id,
            "group_name": l.group_name,
            "title": l.title
        }
        for l in lessons
    ]

    return jsonify(result), 200
