# *-* coding: utf-8 *-*

import logging
import webapp2
import webob.multidict
import uuid
from webapp2_extras import jinja2, auth, sessions
from jinja2.runtime import TemplateNotFound
from libs.simpleauth import SimpleAuthHandler, AuthProviderResponseError
from config import config


def csrf_token():
    session = sessions.get_store().get_session()
    ctn = config['csrf_token_name']
    if ctn not in session:
        session[ctn] = uuid.uuid1().hex
    return session[ctn]


def jinja2_factory(app):
    j = jinja2.Jinja2(app)
    j.environment.globals.update({
        'csrf_token': csrf_token(),
        'uri_for': webapp2.uri_for
    })
    return j


class CSRFException(Exception):
    pass


class ViewContext:

    """
        Shortcut to pass variables to templates
    """
    pass


class BaseHandler(webapp2.RequestHandler):

    """
    """

    def __init__(self, request, response):
        self.initialize(request, response)
        self.view = ViewContext()

    def dispatch(self):
        """
            Get a session store for this request.
        """
        self.session_store = sessions.get_store(request=self.request)

        try:
            # do requirements check here...
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    @webapp2.cached_property
    def messages(self, key='_default'):
        return self.session.get_flashes(key=key)

    @webapp2.cached_property
    def add_message(self, message, level=None, key='_default'):
        """level: An optional level to set with the message. Default is `None`.
        """
        self.session.add_flash(message, level, key=key)

    @webapp2.cached_property
    def user(self):
        """session user
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user_id(self):
        return self.current_user.key.id() if self.user else None

    @webapp2.cached_property
    def current_user(self):
        user = self.auth.get_user_by_session()
        if user:
            return self.auth.store.user_model.get_by_id(user['user_id'])
        return None

    def head(self, *args):
        """Head is used by Twitter. If not there the tweet button shows 0"""
        pass

    def _handle_exception(self, exception, debug):
        """
        override handle_exception method
        """
        logging.exception(exception)
        if not debug:
            return self.render('error', exception="Something goes wrong.")
        raise

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=jinja2_factory, app=self.app)

    def render_template(self, filename, **kwargs):

        if hasattr(self, 'view'):
            kwargs.update(self.view.__dict__)

        kwargs.update({
            'google_analytics_code': self.app.config.get('google_analytics_code'),
            'project_name': self.app.config.get('project_name'),
            'current_user': self.current_user,
            'logged_in': self.auth.get_user_by_session(),
            'url': self.request.url,
            'path': self.request.path,
            'query_string': self.request.query_string,
        })
        if hasattr(self, 'form'):
            kwargs['form'] = self.form
        if self.messages:
            kwargs['messages'] = self.messages

        self.response.headers.add_header('X-UA-Compatible', 'IE=Edge,chrome=1')
        try:
            self.response.write(self.jinja2.render_template(filename, **kwargs))
        except TemplateNotFound:
            self.about(404)

    def render(self, template_name, **kwargs):
        """ A shortcut to render_template
        """
        self.render_template(template_name + '.html', **kwargs)


class AuthHandler(BaseHandler, SimpleAuthHandler):

    def dispatch(self):
        """
            Get a session store for this request.
        """
        self.session_store = sessions.get_store(request=self.request)

        try:
            # do requirements check here...
            webapp2.RequestHandler.dispatch(self)
        except AuthProviderResponseError as ex:
            logging.exception(ex)
            self.redirect('/')
        finally:
            self.session_store.save_sessions(self.response)

    def _on_signin(self, user_info_dict, auth_info, provider, extra=None):
        """Callback whenever a new or existing user is logging in.
         data is a user info dictionary.
         auth_info contains access token or oauth token and secret.
         extra is a dict with additional params passed to the auth init handler.
        """

        try:
            auth_id = '%s:%s' % (provider, user_info_dict['id'])
        except KeyError:
            logging.debug(user_info_dict)
            self.handle_exception(Exception(user_info_dict))
        logging.debug('Looking for a user with id %s', auth_id)

        user = self.auth.store.user_model.get_by_auth_id(auth_id)
        _attrs = self._to_user_model_attrs(user_info_dict, self.app.config['simple_auth_user_attrs'][provider])
        logging.info(_attrs)
        if user:
            # found existing user
            logging.debug('Found existing user to log in')
            # Check if we need to update user data.
            # Here we update the user if there are extra attrs.
            # In this way, we associate user with new attribute from new auth provider.
            # You can use different strategy here.
            _extra_attrs = self._get_extra_attr(user, _attrs)
            logging.info(_extra_attrs)
            if _extra_attrs:
                user.populate(**_extra_attrs)
                user.put()
            self.login_user(user)
        else:
            if self.user:
                # user already logged in
                logging.debug('Updating currently logged in user')
                user_by_user_id = self.current_user
                user_by_user_id.populate(**_attrs)
                ok, _ = user_by_user_id.add_auth_id(auth_id)  # contains a .put()
                if not ok:
                    return self.handle_exception(Exception('Fail to update logged in user {0}'.format(auth_id)))
            else:
                logging.debug('Creating a new user')
                ok, user = self.auth.store.user_model.create_user(auth_id, **_attrs)
                if ok:
                    self.login_user(user)
                else:
                    return self.handle_exception(Exception('Fail to create user {0}'.format(auth_id)))

        # redirect to user page, e.g. '/profile'
        destination_url = '/'
        if extra is not None:
            params = webob.multidict.MultiDict(extra)
            destination_url = str(params.get('destination_url', '/'))
        return self.redirect(destination_url)

    def login_user(self, user):
        return self.auth.set_session(self.auth.store.user_to_dict(user))

    def logout(self):
        self.auth.unset_session()
        self.redirect('/')

    def _callback_uri_for(self, provider):
        return self.uri_for('auth_callback', provider=provider, _full=True)

    def _get_consumer_info_for(self, provider):
        """Returns a tuple (key, secret) for auth init requests."""
        return self.app.config['simple_auth_secrets'][provider]

    def _get_optional_params_for(self, provider):
        """Returns optional parameters for auth init requests."""
        return self.app.config['simple_auth_optional_params'].get(provider)

    def _get_extra_attr(self, user, attrs):
        extra_attrs = {}
        for k, v in attrs.iteritems():
            if not hasattr(user, k):
                logging.debug('{0} needs to be updated to {1}'.format(k, v))
                extra_attrs.setdefault(k, v)
        return extra_attrs

    def _to_user_model_attrs(self, user_info_dict, attr_maps):
        """Get the needed information from provider dataset
        """
        user_attrs = {}
        for k, v in attr_maps.iteritems():
            if isinstance(v, str):
                attr = v, user_info_dict.get(k)
            else:
                attr = v(user_info_dict.get(k))
            user_attrs.setdefault(*attr)

        return user_attrs
