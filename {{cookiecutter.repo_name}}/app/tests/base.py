import unittest
import webapp2
from webtest import TestApp
from config import config
from routes import routes
from webapp2_extras.securecookie import SecureCookieSerializer

app = webapp2.WSGIApplication(routes, config=config)
secure_cookie_serializer = SecureCookieSerializer(
    config['webapp2_extras.sessions']['secret_key'])


class Helper():

    """
    A helper to let TestCase make requests with pre-defined headers and csrf
    """

    def get(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
        return self.app.get(*args, **kwargs)

    def post(self, url, params, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
        if 'csrf' in kwargs and kwargs['csrf'] == True and self.csrf_data:
            if params and isinstance(params, dict) and self.csrf_token_name not in params:
                params.update(**self.csrf_data)
            elif 'params' in kwargs and self.csrf_token_name not in params['kwargs']:
                kwargs['params'].update(**self.csrf_data)
            del kwargs['csrf']
        return self.app.post(url, params, *args, **kwargs)


class BaseTestCase(unittest.TestCase, Helper):

    """
    A Base TestCase to be inherited with session and csrf support.

        Example making a post request in test method:

        def test_index(self):
            self.post('/', {'param':'value'}, csrf=True)

    """

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self._csrf_token = '_csrf'
        self.csrf_token_name = config['csrf_token_name']
        self.csrf_data = {self.csrf_token_name: self._csrf_token}
        serialized = secure_cookie_serializer.serialize('session', self.csrf_data)
        self.headers = {'Cookie': 'session={0}'.format(serialized),
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) Version/6.0 Safari/536.25',
                        'Accept-Language': 'en_US'}
        self.app = TestApp(app, extra_environ={'REMOTE_ADDR': '127.0.0.1'})


class AppTestCase(BaseTestCase):

    """
    A Base TestCase to be inherited with app engine testing utilities support.
    Requirement:
        pip install NoseGAE
    Run tests:
        nosetests --with-gae

    Add more testing utilities if needed.
    (https://cloud.google.com/appengine/docs/python/tools/localunittesting)
    """

    def setUp(self):
        super(AppTestCase, self).setUp()
        # images stub requires PIL
        try:
            import PIL
            self.testbed.init_images_stub()
        except ImportError:
            pass

        self.testbed.init_mail_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_blobstore_stub()
        self.testbed.init_user_stub()

        self.testbed.init_channel_stub()
        self.testbed.init_files_stub()
        self.testbed.init_xmpp_stub()
        self.testbed.init_logservice_stub()
        self.testbed.init_capability_stub()
        self.testbed.init_app_identity_stub()

        try:
            from google.appengine.api.search.simple_search_stub import SearchServiceStub
            self.testbed._register_stub('search', SearchServiceStub())
        except ImportError:
            pass
