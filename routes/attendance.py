from flask import Blueprint, request, jsonify
from models import Attendance, Lesson, Student
from database import db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    if not data or not all(k in data for k in ('lesson_id', 'student_id', 'date', 'present')):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        attendance_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    if not Lesson.query.get(data['lesson_id']):
        return jsonify({'error': 'Lesson not found'}), 404
    if not Student.query.get(data['student_id']):
        return jsonify({'error': 'Student not found'}), 404

    existing_record = Attendance.query.filter_by(
        lesson_id=data['lesson_id'],
        student_id=data['student_id'],
        date=attendance_date
    ).first()

    if existing_record:
        return jsonify({'error': 'Attendance already recorded for this date'}), 409

    new_attendance = Attendance(
        lesson_id=data['lesson_id'],
        student_id=data['student_id'],
        date=attendance_date,
        present=data['present']
    )
    db.session.add(new_attendance)
    db.session.commit()
    return jsonify({'message': 'Attendance recorded successfully'}), 201

@attendance_bp.route('/lesson/<int:lesson_id>/date/<date>', methods=['GET'])
def get_attendance(lesson_id, date):
    try:
        attendance_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    records = Attendance.query.filter_by(lesson_id=lesson_id, date=attendance_date).all()
    return jsonify([
        {
            'student_id': r.student_id,
            'present': r.present
        } for r in records
    ]), 200
