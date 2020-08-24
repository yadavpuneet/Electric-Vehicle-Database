#!/usr/bin/env python
import math
import sys

import webapp2
import jinja2
from google.appengine.api import users
import os

from google.appengine.ext import ndb

from ev import EV

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        # pull the current user from the request
        user = users.get_current_user()

        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
        # generate a map that contains everything that we need to pass to the template
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'evs': EV.query()
        }

        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class AddHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template('add.html')
            template_values = {
                'user': user,
                'params': {
                    'name': '',
                    'manufacturer': '',
                    'year': '',
                    'battery': '',
                    'wltp': '',
                    'power': '',
                    'cost': ''
                }
            }
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        user = users.get_current_user()
        if user:
            params = self.request
            # ev_key = ndb.Key(EV, params.get('name'))
            ev_obj = EV.query(EV.name== params.get('name')).fetch()
            if not ev_obj:
                ev_obj = EV()
                ev_obj.name = params.get('name')
                ev_obj.manufacturer = params.get('manufacturer')
                ev_obj.year = int(params.get('year'))
                ev_obj.battery = int(params.get('battery'))
                ev_obj.wltp = int(params.get('wltp'))
                ev_obj.power = int(params.get('power'))
                ev_obj.cost = float(params.get('cost'))
                ev_obj.put()
                template_values = {
                    'user': user,
                    'report': '1',
                    'params': {'name': '', 'manufacturer': ''}
                }
            else:
                template_values = {
                    'user': user,
                    'report': '2',
                    'params': self.request
                }
            template = JINJA_ENVIRONMENT.get_template('add.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')


class QueryHandler(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('query.html')
        template_values = {
        }
        self.response.write(template.render(template_values))

    def post(self):
        params = self.request
        name = params.get('name')
        manufacturer = params.get('manufacturer')
        year_lc = int(params.get('year-lc-t'))
        year_uc = int(params.get('year-uc-t'))
        battery_lc = int(params.get('battery-lc-t'))
        battery_uc = int(params.get('battery-uc-t'))
        wltp_lc = int(params.get('wltp-lc-t'))
        wltp_uc = int(params.get('wltp-uc-t'))
        power_lc = int(params.get('power-lc-t'))
        power_uc = int(params.get('power-uc-t'))
        cost_lc = int(params.get('cost-lc-t'))
        cost_uc = int(params.get('cost-uc-t'))

        query = EV.query().fetch(keys_only=True)
        if len(name.strip()) > 0:
            query = set(query).intersection(EV.query(EV.name == name.strip()).fetch(keys_only=True))
        if len(manufacturer.strip()) > 0:
            query = set(query).intersection(EV.query(EV.manufacturer == manufacturer.strip()).fetch(keys_only=True))
        query = set(query).intersection(EV.query(EV.year >= year_lc, EV.year <= year_uc).fetch(keys_only=True))
        query = set(query).intersection(
            EV.query(EV.battery >= battery_lc, EV.battery <= battery_uc).fetch(keys_only=True))
        query = set(query).intersection(EV.query(EV.wltp >= wltp_lc, EV.wltp <= wltp_uc).fetch(keys_only=True))
        query = set(query).intersection(EV.query(EV.power >= power_lc, EV.power <= power_uc).fetch(keys_only=True))
        query = set(query).intersection(EV.query(EV.cost >= cost_lc, EV.cost <= cost_uc).fetch(keys_only=True))
        result = ndb.get_multi(query)
        if not result:
            result = None
        else:
            result.sort(key=lambda x: x.name, reverse=False)

        template_values = {
            'result': result
        }
        template = JINJA_ENVIRONMENT.get_template('query.html')
        self.response.write(template.render(template_values))


class DetailsHandler(webapp2.RequestHandler):
    def get(self):
        ev = ndb.Key(urlsafe=self.request.get('id')).get()
        template = JINJA_ENVIRONMENT.get_template('details.html')
        template_values = {
            'ev': ev,
            'user': users.get_current_user()
        }
        self.response.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()
        if user:
            params = self.request
            ev_obj = EV.query(EV.name == params.get('name').strip()).fetch()
            if not ev_obj:
                print self.request.get('id')
                ev_obj = ndb.Key(urlsafe=self.request.get('id')).get()
                ev_obj.name = params.get('name')
                ev_obj.manufacturer = params.get('manufacturer')
                ev_obj.year = int(params.get('year'))
                ev_obj.battery = int(params.get('battery'))
                ev_obj.wltp = int(params.get('wltp'))
                ev_obj.power = int(params.get('power'))
                ev_obj.cost = float(params.get('cost'))
                ev_obj.put()
                template_values = {
                    'ev': ev_obj,
                    'user': user,
                    'report': '1',
                    'params': {'name': '', 'manufacturer': ''}
                }
            else:
                template_values = {
                    'ev': ev_obj[0],
                    'user': user,
                    'report': '2',
                    'params': self.request
                }
            template = JINJA_ENVIRONMENT.get_template('details.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')


class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        ev = ndb.Key(urlsafe=self.request.get('id')).get()
        ev.key.delete()
        template_values = {
            "delete": True
        }
        template = JINJA_ENVIRONMENT.get_template('query.html')
        self.response.write(template.render(template_values))


class CompareHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            "evs": EV.query().order(EV.name)
        }
        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))

    def post(self):

        evs = []
        for p in self.request.params:
            evs.append(ndb.Key(urlsafe=p).get())
        maxs = {}
        mins = {}

        for ev in evs:
            try:
                maxs['rating'] = max(float(sum(ev.ratings)) / len(ev.ratings), maxs.get('rating', 0))
            except:
                pass
            maxs['battery'] = max(ev.battery, maxs.get('battery', 0))
            maxs['wltp'] = max(ev.wltp, maxs.get('wltp', 0))
            maxs['power'] = max(ev.power, maxs.get('power', 0))
            maxs['cost'] = max(ev.cost, maxs.get('cost', 0))

            try:
                mins['rating'] = min(float(sum(ev.ratings)) / len(ev.ratings), float(mins.get('rating', sys.maxint)))
            except:
                pass
            mins['battery'] = min(ev.battery, mins.get('battery', sys.maxint))
            mins['wltp'] = min(ev.wltp, mins.get('wltp', sys.maxint))
            mins['power'] = min(ev.power, mins.get('power', sys.maxint))
            mins['cost'] = min(ev.cost, mins.get('cost', sys.maxint))

        print maxs
        print mins

        template_values = {
            "evs": EV.query().order(EV.name),
            "compare": evs,
            'maxs': maxs,
            'mins': mins
        }
        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))


class ReviewsHandler(webapp2.RequestHandler):
    def get(self):
        ev = ndb.Key(urlsafe=self.request.get('id')).get()
        template_values = {
            "reviews": ev.reviews,
            "ratings": ev.ratings,
            "ev": ev,
            "user": users.get_current_user()
        }
        template = JINJA_ENVIRONMENT.get_template('reviews.html')
        self.response.write(template.render(template_values))

    def post(self):
        ev = ndb.Key(urlsafe=self.request.get('id')).get()
        ev.reviews.append(self.request.get('review'))
        ev.ratings.append(int(self.request.get('rating')))
        ev.put()
        template_values = {
            "report": 1,
            "reviews": ev.reviews,
            "ratings": ev.ratings,
            "ev": ev,
            "user": users.get_current_user()
        }
        template = JINJA_ENVIRONMENT.get_template('reviews.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add', AddHandler),
    ('/query', QueryHandler),
    ('/details', DetailsHandler),
    ('/update', DetailsHandler),
    ('/delete', DeleteHandler),
    ('/compare', CompareHandler),
    ('/reviews', ReviewsHandler),
], debug=True)
