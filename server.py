import cherrypy
import pymysql
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

class HelloWorld(object):
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render()



    index.exposed = True

cherrypy.quickstart(HelloWorld(), config='server.conf')
