from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Define database models here
# ...

# Routes for User APIs
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(result), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'id': user.id, 'username': user.username}), 200

# Routes for Course APIs
@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    result = [{'id': course.id, 'name': course.name} for course in courses]
    return jsonify(result), 200

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404
    return jsonify({'id': course.id, 'name': course.name}), 200

# Routes for Student APIs
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = [{'id': student.id, 'name': student.name, 'course_id': student.course_id} for student in students]
    return jsonify(result), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    return jsonify({'id': student.id, 'name': student.name, 'course_id': student.course_id}), 200

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', filename='app.log', filemode='a')

@app.route('/')
def index():
    app.logger.info('Home page accessed')
    return 'Welcome to the Attendance Management System'

# Rest of the code...

def create_first_user():
    user_count = User.query.count()
    if user_count == 0:
        # Create the first user
        first_user = User(username='admin', password='admin')
        db.session.add(first_user)
        db.session.commit()

        # Display password in logs
        app.logger.info(f'First user created. Username: {first_user.username}, Password: {first_user.password}')

@app.before_request
def before_first_request():
    if not app.config.get('INITIALIZED'):
        create_first_user()
        app.config['INITIALIZED'] = True

# Rest of the code...

if __name__ == '__main__':
    app.run()
