@attendance_bp.route('/', methods=['GET'])
def get_attendance_records():
    lesson_id = request.args.get('lesson_id', type=int)
    date_from_str = request.args.get('date_from')
    date_to_str = request.args.get('date_to')

    if not all([lesson_id, date_from_str, date_to_str]):
        return jsonify({'error': 'Missing required query parameters: lesson_id, date_from, date_to'}), 400

    try:
        date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404

    attendance_records = Attendance.query.filter(
        Attendance.lesson_id == lesson_id,
        Attendance.date >= date_from,
        Attendance.date <= date_to
    ).all()

    records_data = [
        {
            'student_id': ar.student_id,
            'lesson_id': ar.lesson_id,
            'date': ar.date.strftime('%Y-%m-%d'),
            'present': ar.present
        }
        for ar in attendance_records
    ]
    return jsonify(records_data), 200

@attendance_bp.route('/', methods=['POST'])
def toggle_attendance_record():
    data = request.get_json()
    if not data or not all(k in data for k in ('lesson_id', 'student_id', 'date', 'present')):
        return jsonify({'error': 'Missing required fields: lesson_id, student_id, date, present'}), 400

    lesson_id = data['lesson_id']
    student_id = data['student_id']
    present = data['present'] # Булеве значення

    try:
        attendance_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format for attendance. Use YYYY-MM-DD.'}), 400

    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    # Перевірка, чи існує запис відвідуваності для цієї дати, заняття та студента
    existing_record = Attendance.query.filter_by(
        lesson_id=lesson_id,
        student_id=student_id,
        date=attendance_date
    ).first()

    if existing_record:
        # Оновлюємо існуючий запис
        existing_record.present = present
        db.session.commit()
        return jsonify({'message': 'Attendance record updated successfully', 'id': existing_record.id}), 200
    else:
        # Створюємо новий запис
        new_record = Attendance(
            lesson_id=lesson_id,
            student_id=student_id,
            date=attendance_date,
            present=present
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': 'Attendance record created successfully', 'id': new_record.id}), 201
