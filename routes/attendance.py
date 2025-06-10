from flask import Blueprint, request, jsonify
from models import Attendance, Lesson, Student
from database import db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    for k in ('lesson_id','student_id','date','present'):
        if k not in data:
            return jsonify({'error': f'Missing {k}'}), 400

    try:
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    if not Lesson.query.get(data['lesson_id']) or not Student.query.get(data['student_id']):
        return jsonify({'error': 'Lesson or Student not found'}), 404

    rec = Attendance.query.filter_by(
        lesson_id=data['lesson_id'],
        student_id=data['student_id'],
        date=date_obj
    ).first()
    if rec:
        rec.present = data['present']
        msg = 'updated'
    else:
        rec = Attendance(
            lesson_id=data['lesson_id'],
            student_id=data['student_id'],
            date=date_obj,
            present=data['present']
        )
        db.session.add(rec)
        msg = 'created'

    db.session.commit()
    return jsonify({'message': f'Attendance {msg}.'}), 200

@attendance_bp.route('/lesson/<int:lesson_id>/dates', methods=['GET'])
def get_lesson_attendance_dates(lesson_id):
    dates = (
        db.session.query(Attendance.date)
        .filter_by(lesson_id=lesson_id)
        .distinct()
        .order_by(Attendance.date)
        .all()
    )
    return jsonify([d[0].isoformat() for d in dates]), 200


@attendance_bp.route('/lesson/<int:lesson_id>/date/<date>', methods=['GET'])
def get_attendance_by_date(lesson_id, date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    recs = Attendance.query.filter_by(lesson_id=lesson_id, date=date_obj).all()
    return jsonify([{'student_id': r.student_id, 'present': r.present} for r in recs]), 200
