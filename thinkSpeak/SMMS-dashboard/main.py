import cherrypy
import os

class Example(object):
	"""docstring for Reverser"""
	exposed=True
	def __init__(self):
		self.id=1
	def GET(self):
		return open("dashboard.html")


if __name__ == '__main__':
	conf={
		'/':{
				'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
				'tools.staticdir.root': os.path.abspath(os.getcwd()),
			},
		 '/assets':{
		 'tools.staticdir.on': True,
		 'tools.staticdir.dir':'./assets'
		 },
	}

	cherrypy.tree.mount(Example(),'/',conf)
	cherrypy.config.update({'server.socket_port': 8080})
	cherrypy.engine.start()
	cherrypy.engine.block()
