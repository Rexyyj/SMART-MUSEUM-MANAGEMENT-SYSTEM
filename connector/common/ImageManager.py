import cherrypy
import json

class ImageManager():
    exposed = True

    def __init__(self,folder):
        self.folder = folder

    def GET(self):
        pass

