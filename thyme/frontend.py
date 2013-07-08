from datetime import date, datetime

import cherrypy
from jinja2 import Environment, FileSystemLoader

from .database import init_db, Entry
from .settings import TEMPLATE_DIR


class ThymeFace:
    def index(self):
        today = date.today()
        today_start = datetime(today.year, today.month, today.day, 0, 0, 0)
        today_end = datetime(today.year, today.month, today.day, 23, 59, 59)

        entries = self.db.query(Entry). \
            filter(Entry.time >= today_start, Entry.time <= today_end). \
            order_by(Entry.time)

        template = self.env.get_template('frontend.html')
        return template.render(entries=entries)

    def __init__(self, db):
        self.db = db
        self.env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    index.exposed = True


def launch_frontend():
    cherrypy.config.update({'server.thread_pool': 1})
    cherrypy.quickstart(ThymeFace(db=init_db()))
