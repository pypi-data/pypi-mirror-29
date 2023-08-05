#!/usr/bin/env python

import os
import pkgutil
import random
import sys
import getpass

from flask_script import Manager, Command, Option
from flask_migrate import Migrate, MigrateCommand
from jinja2 import Template
from werkzeug.security import generate_password_hash

from ihatemoney.run import create_app
from ihatemoney.models import db


class GeneratePasswordHash(Command):

    """Get password from user and hash it without printing it in clear text."""

    def run(self):
        password = getpass.getpass(prompt='Password: ')
        print(generate_password_hash(password))


class GenerateConfig(Command):
    def get_options(self):
        return [
            Option('config_file', choices=[
                'ihatemoney.cfg',
                'apache-vhost.conf',
                'gunicorn.conf.py',
                'supervisord.conf',
                'nginx.conf',
            ]),
        ]

    @staticmethod
    def gen_secret_key():
        return ''.join([
            random.SystemRandom().choice(
                'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
            for i in range(50)])

    def run(self, config_file):
        template_content = pkgutil.get_data(
            'ihatemoney',
            os.path.join('conf-templates/', config_file) + '.j2'
        ).decode('utf-8')

        print(Template(template_content).render(
                pkg_path=os.path.abspath(os.path.dirname(__file__)),
                venv_path=os.environ.get('VIRTUAL_ENV'),
                secret_key=self.gen_secret_key(),
        ))


def main():
    QUIET_COMMANDS = ('generate_password_hash', 'generate-config')

    backup_stderr = sys.stderr
    # Hack to divert stderr for commands generating content to stdout
    # to avoid confusing the user
    if len(sys.argv) > 1 and sys.argv[1] in QUIET_COMMANDS:
        sys.stderr = open(os.devnull, 'w')

    app = create_app()
    Migrate(app, db)

    # Restore stderr (among other: to be able to display help)
    sys.stderr = backup_stderr

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.add_command('generate_password_hash', GeneratePasswordHash)
    manager.add_command('generate-config', GenerateConfig)
    manager.run()


if __name__ == '__main__':
    main()
