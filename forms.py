from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddForm(FlaskForm):
    name = StringField('Name:')
    submit = SubmitField('Add Student')


class DelForm(FlaskForm):
    id = IntegerField('Student ID:')
    submit = SubmitField('Remove Student')


class AddReportForm(FlaskForm):
    status_description = StringField("Status: ")
    stu_id = IntegerField("Student ID: ")
    submit = SubmitField("Add Report")


class AddGradeForm(FlaskForm):
    homework_name = StringField("Homework's name: ")
    homework_grade = IntegerField("Grade: ")
    stu_id = IntegerField("Student ID: ")
    submit = SubmitField("Add Grade")
