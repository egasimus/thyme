from multiprocessing import Process

import cherrypy

from .database import init_db, Entry


class ThymeFace:
    def index(self):
        s = "Time spent in:<br />"
        for e in self.db.query(Entry).order_by(Entry.time):
            s += "%s %s %s<br />" % (e.id, e.title, e.time)
        return s

    def __init__(self, db):
        self.db = db
    index.exposed = True


def frontend():
    cherrypy.quickstart(ThymeFace(db=init_db()))


def launch_frontend():
    p = Process(target=frontend)
    p.start()
    return p
