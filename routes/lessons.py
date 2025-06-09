from flask import Blueprint, request, jsonify
from models import Lesson, Group
from database import db

lessons_bp = Blueprint('lessons', __name__)

@lessons_bp.route('/', methods=['POST'])
def create_lesson():
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'group_id', 'days')):
        return jsonify({'error': 'Missing required fields'}), 400

    title = data['title'].strip()
    group_id = data['group_id']
    days = data['days']

    if not title:
        return jsonify({'error': 'Назва заняття не може бути порожньою'}), 400
    if not days:
        return jsonify({'error': 'Потрібно вибрати хоча б один день'}), 400

    if not Group.query.get(group_id):
        return jsonify({'error': 'Group not found'}), 404

    # Перевірка на існуюче заняття з такою ж назвою в цій групі
    existing_lesson = Lesson.query.filter_by(group_id=group_id, title=title).first()
    if existing_lesson:
        return jsonify({'error': 'Заняття з такою назвою вже існує'}), 400

    try:
        new_lesson = Lesson(title=title, group_id=group_id)
        db.session.add(new_lesson)
        db.session.flush()  # Отримати lesson.id до коміту

        for day in days:
            lesson_day = LessonDay(lesson_id=new_lesson.id, day_of_week=day)
            db.session.add(lesson_day)

        db.session.commit()
        return jsonify({'message': 'Заняття створено успішно', 'lesson_id': new_lesson.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Помилка при створенні заняття: {str(e)}'}), 500

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

@lessons_bp.route('/<int:lesson_id>', methods=['DELETE'])
def delete_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({'error': 'Заняття не знайдено'}), 404

    try:
        db.session.delete(lesson)
        db.session.commit()
        return jsonify({'message': 'Заняття успішно видалено'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Не вдалося видалити заняття'}), 500

@lessons_bp.route('/<int:lesson_id>/days', methods=['GET'])
def get_lesson_days(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404

    days = LessonDay.query.filter_by(lesson_id=lesson_id).all()
    return jsonify([day.day_of_week for day in days]), 200
