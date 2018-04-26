#/usr/bin/env python
import os
from app import create_app, db
from app.models import Team, Match, Flagged, Country, League
from flask_script import Shell, Manager, Server
from flask_migrate import MigrateCommand, Migrate


app = create_app(os.getenv('CONFIGURATION') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_content():
    return dict(app=app, db=db, Team=Team, Match=Match, Flagged=Flagged, Country=Country, League=League)

manager.add_command('runserver', Server(host='0.0.0.0', port='9000')) # use when developing on codeanywhere
manager.add_command('shell', Shell(make_context=make_shell_content))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()