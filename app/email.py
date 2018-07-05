""" 
functions: integrate email servicing functionalities

include sending reports to a list of subscribed email addresses

"""
from .models import SubscribedEmail, db
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import FlushError


def add_email(subscribed_email):
    try:
        new_subscriber = SubscribedEmail(email=subscribed_email)
        db.session.add(new_subscriber)
        db.session.commit()
    except(FlushError, IntegrityError, InvalidRequestError):
        db.session.rollback()
        return {
            'status': 'bad',
            'message': 'Email is already subscribed'
        }
    return {
        'status': 'ok',
        'message': 'Email succesfully subscribed'
    }