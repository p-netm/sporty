"""
 Defines the various errors that the client or the server may run into

    Questions?-> what is the e in the below eror handler route functions
"""
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    """defines the template for a resource that cannot be found"""
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Show internal problecms and this is one that we do not want"""
    return render_template('500.html'), 500