from multiprocessing import Process

import cherrypy


class ThymeFace:
    def index(self):
        return "Hello world!"
    index.exposed = True


def launch_frontend():
    p = Process(target=cherrypy.quickstart, args=(ThymeFace(),))
    return p
