from flask import Flask
from flask_cors import CORS
from config import Config
from database import db

# Імпортуємо блакпринти
from routes.auth import auth_bp
from routes.groups import groups_bp
from routes.lessons import lessons_bp
from routes.students import students_bp
from routes.attendance import attendance_bp
from routes.user import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    # Імпорт моделей після ініціалізації db
    from models import User, Group, Student, Lesson, LessonDay, Attendance

    # Створюємо таблиці, якщо ще не існують
    with app.app_context():
        db.create_all()

    # Реєструємо маршрути
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(groups_bp, url_prefix='/groups')
    app.register_blueprint(lessons_bp, url_prefix='/lessons')
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(user_bp, url_prefix='/user')

    return app

# Створення об'єкта Flask, необхідного для gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
