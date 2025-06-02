from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    groups = db.relationship('Group', backref='user', cascade='all, delete', lazy=True)


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    students = db.relationship('Student', backref='group', cascade='all, delete', lazy=True)
    lessons = db.relationship('Lesson', backref='group', cascade='all, delete', lazy=True)


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    attendance = db.relationship('Attendance', backref='student', cascade='all, delete', lazy=True)


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)

    lesson_days = db.relationship('LessonDay', backref='lesson', cascade='all, delete', lazy=True)
    attendance = db.relationship('Attendance', backref='lesson', cascade='all, delete', lazy=True)


class LessonDay(db.Model):
    __tablename__ = 'lesson_days'

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    present = db.Column(db.Boolean, nullable=False)

    __table_args__ = (db.UniqueConstraint('lesson_id', 'student_id', 'date', name='_lesson_student_date_uc'),)
