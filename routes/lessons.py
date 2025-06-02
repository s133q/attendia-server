from flask import Blueprint, jsonify
from models import Lesson

lessons_bp = Blueprint('lessons', __name__)

@lessons_bp.route('/', methods=['GET'])
def get_lessons():
    lessons = Lesson.query.all()
    return jsonify([{'id': l.id, 'title': l.title} for l in lessons])

