import os

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    os.path.pardir
))

DB_PATH = 'sqlite:///%s/db.sqlite' % PROJECT_ROOT
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
POLL_INTERVAL = 0.5
