from flask import Blueprint, request, jsonify
from models import Attendance
from database import db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/', methods=['GET'])
def get_attendance():
    lesson_id = request.args.get('lesson_id')
    if not lesson_id:
        return {'error': 'Missing lesson_id'}, 400

    records = Attendance.query.filter_by(lesson_id=lesson_id).all()
    return jsonify([
        {
            'student_id': r.student_id,
            'date': r.date.isoformat(),
            'present': r.present
        } for r in records
    ])

@attendance_bp.route('/', methods=['POST'])
def post_attendance():
    data = request.json
    required_fields = ['lesson_id', 'student_id', 'date', 'present']
    if not all(field in data for field in required_fields):
        return {'error': 'Missing fields'}, 400

    date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
    record = Attendance.query.filter_by(
        lesson_id=data['lesson_id'],
        student_id=data['student_id'],
        date=date_obj
    ).first()

    if record:
        record.present = data['present']
    else:
        record = Attendance(
            lesson_id=data['lesson_id'],
            student_id=data['student_id'],
            date=date_obj,
            present=data['present']
        )
        db.session.add(record)

    db.session.commit()
    return {'message': 'Attendance record updated'}
