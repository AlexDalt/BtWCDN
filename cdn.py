import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
import time


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
    votes_for = ndb.IntegerProperty(indexed=False,repeated=True)
    votes_against = ndb.IntegerProperty(indexed=False,repeated=True)


class DemoForm(webapp2.RequestHandler):
    def get(self):
        self.response.write("index.html")

class Submit(webapp2.RequestHandler):
    def post(self):
        application = Application()

        #need to force absolute urls
        application.name = self.request.get('band_name')
        application.hometown = self.request.get('hometown')
        application.facebook = self.request.get('facebook')
        application.soundcloud = self.request.get('soundcloud')
        application.contact = self.request.get('contact')
        application.votes_for = []
        application.votes_against = []

        application.put()

        self.redirect('/')

class Review(webapp2.RequestHandler):
    def get(self):
        applications_query = Application.query()
        applications = applications_query.fetch()
        template_values = {'applications': applications}
        template = JINJA_ENVIRONMENT.get_template('review.html')
        self.response.write(template.render(template_values))

class Vote(webapp2.RequestHandler):
    def post(self):
        # get user ID, store that in a list on data object
        user_id = 1;
        band_key = ndb.Key(urlsafe=self.request.get('band_key'))

        application = band_key.get()

        if( self.request.get('vote') == "yes" ):
            if user_id in application.votes_against:
                application.votes_against.remove(user_id)
            if user_id not in application.votes_for:
                application.votes_for.append(user_id)
        elif( self.request.get('vote') == "no" ):
            if user_id in application.votes_for:
                application.votes_for.remove(user_id)
            if user_id not in application.votes_against:
                application.votes_against.append(user_id)

        application.put()
        time.sleep(0.2)
        self.redirect('/review')


app = webapp2.WSGIApplication([
    ('/',DemoForm),
    ('/submit', Submit),
    ('/review', Review),
    ('/vote', Vote),
],debug=True)
