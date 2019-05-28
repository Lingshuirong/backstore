from backstage import get_app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


app = get_app('dev')
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
