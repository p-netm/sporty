#/usr/bin/env python
import os
from app import create_app, db
from app.models import Team, Match
from flask_script import Shell, Manager
from flask_migrate import MigrateCommand, Migrate


app = create_app(os.getenv('CONFIGURATION') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_content():
    return dict(app=app, db=db, Team=Team, Match=Match)
manager.add_command('shell', Shell(make_context=make_shell_content))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()