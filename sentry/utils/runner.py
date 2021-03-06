#!/usr/bin/env python
"""
sentry.utils.runner
~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from logan.runner import run_app
from sentry import environment

import base64
import datetime
import os

KEY_LENGTH = 40

CONFIG_TEMPLATE = """
import os.path

ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        # You can swap out the engine for MySQL easily by changing this value
        # to ``django.db.backends.mysql`` or to PostgreSQL with
        # ``django.db.backends.postgresql_psycopg2``
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT, 'sentry.db'),
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SENTRY_KEY = %(default_key)r

# Set this to false to require authentication
SENTRY_PUBLIC = True

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = 9000
"""


def generate_settings():
    """
    This command is run when ``default_path`` doesn't exist, or ``init`` is
    run and returns a string representing the default data to put into their
    settings file.
    """
    output = CONFIG_TEMPLATE % dict(
        default_key=base64.b64encode(os.urandom(KEY_LENGTH)),
    )

    return output


def initialize_app(config):
    environment['config'] = config.get('config_path')
    environment['start_date'] = datetime.datetime.utcnow()


def main():
    run_app(
        project='sentry',
        default_config_path='~/.sentry/sentry.conf.py',
        default_settings='sentry.conf.defaults',
        settings_initializer=generate_settings,
        settings_envvar='SENTRY_CONF',
        initializer=initialize_app,
    )
