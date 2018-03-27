"""Defines all the form classes that we will be needing

tips subscription form
a date tool for responsiveness -> in small devices
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import Email, DataRequired, InputRequired


class Email(FlaskForm):
    """Template for buildig the email tips subscription form"""
    email = StringField('Email', validators=[DataRequired(), InputRequired(), Email()])
    submit = SubmitField('subscribe')
    
class DateFilter(FlaskForm):
    """Decision pending"""
    pass