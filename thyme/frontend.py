from datetime import date, datetime, timedelta
from random import randrange

import cherrypy
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import desc

from .database import init_db, Entry
from .settings import TEMPLATE_DIR


class ThymeFace(object):
    def index(self):
        today = date.today()
        today_start = datetime(today.year, today.month, today.day, 0, 0, 0)
        today_end = datetime(today.year, today.month, today.day, 23, 59, 59)

        entries = self.db.query(Entry). \
            filter(Entry.time >= today_start, Entry.time <= today_end). \
            order_by(desc(Entry.time))

        timeline = []
        total_time = timedelta(seconds=0)
        end_time = datetime.now()

        for entry in entries:
            duration = end_time - entry.time
            total_time += duration
            end_time = entry.time
            timeline.append({'id': entry.id,
                             'title': entry.title,
                             'duration': duration})

        for entry in timeline:
            width = entry['duration'] / total_time * 100
            entry.update({'width': width,
                          'color': 'rgb(%s,%s,%s)' % (randrange(255),
                                                      randrange(255),
                                                      randrange(255),)})

        template = self.env.get_template('frontend.html')

        context = {
            'timeline': timeline,
            'total_time': total_time
        }

        return template.render(context)

    def __init__(self, db):
        self.db = db
        self.env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    index.exposed = True


def launch_frontend():
    cherrypy.config.update({'server.thread_pool': 1})
    cherrypy.quickstart(ThymeFace(db=init_db()))
