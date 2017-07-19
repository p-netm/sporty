"""Defines all the form classes that we will be needing

1 contact form
2 administration input for things such as the parameters
"""
from flask_wtf import Form
from wtforms import SubmitField


class ContactForm(Form):
    submit = SubmitField('submit')