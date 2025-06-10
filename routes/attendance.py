from flask import Blueprint, request, jsonify
from models import Attendance, Lesson, Student
from database import db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data'}), 400

    student_id = data.get('student_id')
    lesson_id = data.get('lesson_id')
    date_str = data.get('date')
    present = data.get('present')

    if not all([student_id, lesson_id, date_str, present in [True, False]]):
        return jsonify({'error': 'Missing or invalid fields'}), 400

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    attendance = Attendance.query.filter_by(
        student_id=student_id, lesson_id=lesson_id, date=date_obj
    ).first()

    if attendance:
        attendance.present = present
        msg = 'updated'
    else:
        attendance = Attendance(
            student_id=student_id,
            lesson_id=lesson_id,
            date=date_obj,
            present=present
        )
        db.session.add(attendance)
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

@attendance_bp.route('/lesson/<int:lesson_id>/attendance/range', methods=['POST'])
def get_attendance_for_dates(lesson_id):
    try:
        data = request.get_json()
        dates = data.get('dates')
        if not dates or not isinstance(dates, list):
            return jsonify({'error': 'Invalid or missing dates'}), 400

        parsed_dates = []
        for d in dates:
            try:
                parsed_dates.append(datetime.strptime(d, '%Y-%m-%d').date())
            except ValueError:
                return jsonify({'error': f'Invalid date format: {d}'}), 400

        records = (
            db.session.query(Attendance)
            .filter(Attendance.lesson_id == lesson_id, Attendance.date.in_(parsed_dates))
            .all()
        )
        result = [
            {'student_id': r.student_id, 'date': r.date.isoformat(), 'present': r.present}
            for r in records
        ]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
