import webapp2_extras.appengine.auth.models
from google.appengine.ext import ndb
from webapp2_extras import security


class User(webapp2_extras.appengine.auth.models.User):

    """
    Extended user model.
    Compatible with GAE's users API
    """

    username = ndb.StringProperty()
    name = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()  # hashed password
    country = ndb.StringProperty()
    tz = ndb.StringProperty()  # timezone
    avatar_url = ndb.StringProperty()
    activated = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get_by_email(cls, email):
        return cls.query(cls.email == email).get()

    def set_password(self, raw_password):
        self.password = security.generate_password_hash(raw_password)
