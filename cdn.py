import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

class DemoForm(webapp2.RequestHandler):
    def get(self):
        self.response.write("index.html")

class Submit(webapp2.RequestHandler):
    def post(self):
        self.redirect('https://joefest.co.uk/')

app = webapp2.WSGIApplication([
    ('/',DemoForm),
    ('/submit', Submit),
],debug=True)
