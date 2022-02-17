from flask import Flask, render_template, url_for, redirect
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddForm, DelForm, AddReportForm, AddGradeForm

app = Flask(__name__)
# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'

############################################

# SQL DATABASE SET UP AND MODELS

##########################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    performance_report = db.relationship('Report', backref='student', uselist=False)
    homeworks = db.relationship('Homework', backref='student')

    def __init__(self, name):
        self.name = name


class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    grade = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    # Kinda like constructor in Java
    def __init__(self, name, grade, student_id):
        self.name = name
        self.grade = grade
        self.student_id = student_id

    def __repr__(self):
        return f"Homework {self.name} - Homework ID: {self.id} - Grade: {self.grade} \n"


# Weekly performance report
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_description = db.Column(db.Text)
    # can have date column
    # db.ForeignKey('tablename.column_id')
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __init__(self, status_description, student_id):
        self.status_description = status_description
        self.student_id = student_id

    def __repr__(self):
        return f"{self.status_description}"


db.create_all()


############################################

# VIEWS WITH FORMS

##########################################
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add', methods=['GET', 'POST'])
def add_stu():
    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data

        # Add new Student to database
        new_student = Student(name)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('list_stu'))

    return render_template('add_student.html', form=form)


@app.route('/list')
def list_stu():
    # Grab a list of puppies from database.
    students = Student.query.all()

    return render_template('list_student.html', students=students)


@app.route('/delete', methods=['GET', 'POST'])
def del_stu():
    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()

        return redirect(url_for('list_stu'))
    return render_template('delete_student.html', form=form)


@app.route('/report', methods=['GET', 'POST'])
def add_report():
    form = AddReportForm()

    if form.validate_on_submit():
        status_description = form.status_description.data
        stu_id = form.stu_id.data
        # Add new report to database
        new_report = Report(status_description, stu_id)
        db.session.add(new_report)
        db.session.commit()

        return redirect(url_for('list_stu'))

    return render_template('add_report.html', form=form)


@app.route('/add_grade', methods=['GET', 'POST'])
def add_grade():
    form = AddGradeForm()

    if form.validate_on_submit():
        homework_name = form.homework_name.data
        homework_grade = form.homework_grade.data
        stu_id = form.stu_id.data
        # Add new report to database
        new_grade = Homework(homework_name, homework_grade, stu_id)
        db.session.add(new_grade)
        db.session.commit()

        return redirect(url_for('list_stu'))

    return render_template('add_grade.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
