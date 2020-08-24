from google.appengine.ext import ndb


class EV(ndb.Model):
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.IntegerProperty()
    battery = ndb.IntegerProperty()
    wltp = ndb.IntegerProperty()
    cost = ndb.FloatProperty()
    power = ndb.IntegerProperty()
    reviews = ndb.StringProperty(repeated=True)
    ratings = ndb.IntegerProperty(repeated=True)

