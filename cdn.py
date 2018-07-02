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

class Application(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    hometown = ndb.StringProperty(indexed=False)
    facebook = ndb.StringProperty(indexed=False)
    soundcloud = ndb.StringProperty(indexed=False)
    contact = ndb.StringProperty(indexed=False)

    reviewer = ndb.IntegerProperty(indexed=True)
    reviewed = ndb.BooleanProperty(indexed=True)
    shortlisted = ndb.BooleanProperty(indexed=True)

class DemoForm(webapp2.RequestHandler):
    def get(self):
        self.response.write("index.html")

class Submit(webapp2.RequestHandler):
    def post(self):
        application = Application()
        application.name = self.request.get('band_name')
        application.hometown = self.request.get('hometown')
        application.facebook = self.request.get('facebook')
        application.soundcloud = self.request.get('soundcloud')
        application.contact = self.request.get('contact')

        application.reviewer = 0
        application.reviewed = False
        application.shortlisted = False
        application.put()

        self.redirect('/')

class Review(webapp2.RequestHandler):
    def get(self):
        applications_query = Application.query(Application.reviewer == 0)
        applications = applications_query.fetch()
        self.response.write(applications)

app = webapp2.WSGIApplication([
    ('/',DemoForm),
    ('/submit', Submit),
    ('/review', Review),
],debug=True)
