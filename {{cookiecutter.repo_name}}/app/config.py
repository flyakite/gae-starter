# -*- coding: utf-8 -*-

DEFAULT_AVATAR_URL = '/static/img/missing-avatar.png'
FACEBOOK_AVATAR_URL = 'https://graph.facebook.com/{0}/picture?type=large'
FOURSQUARE_USER_LINK = 'http://foursquare.com/user/{0}'

# https://console.developers.google.com
# 1.Add https://<your_website>/auth/googleplus/callback to Redirect URIs
# 2.Enable Google Plus API https://console.developers.google.com/
GOOGLE_APP_ID = ""
GOOGLE_APP_SECRET = ""

# https://developers.facebook.com/apps
FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""

# Key/secret for both LinkedIn OAuth 1.0a and OAuth 2.0
# https://www.linkedin.com/secure/developer
# Add http://<your_website>/auth/linkedin2/callback to Redriect URLs
LINKEDIN_KEY = ""
LINKEDIN_SECRET = ""

# http://go.microsoft.com/fwlink/?LinkID=144070
# Add https://<your_website>/auth/windows_live/callback to Redirect URLs
WL_CLIENT_ID = ""
WL_CLIENT_SECRET = ""

# https://dev.twitter.com/apps
TWITTER_CONSUMER_KEY = ""
TWITTER_CONSUMER_SECRET = ""

# https://foursquare.com/developers/apps
FOURSQUARE_CLIENT_ID = ""
FOURSQUARE_CLIENT_SECRET = ""

config = {

    'project_name': "{{ cookiecutter.project_name }}",

    # https://webapp-improved.appspot.com/_modules/webapp2_extras/sessions.html
    'webapp2_extras.sessions': {'secret_key': '{{ cookiecutter.session_secret_key }}'},

    # https://webapp-improved.appspot.com/_modules/webapp2_extras/auth.html
    'webapp2_extras.auth': {'user_model': 'models.user.User'},

    'webapp2_extras.jinja2': {'template_path': ['templates']},

    'google_analytics_code': "",

    # Derived attributes and User property mapping.
    'simple_auth_user_attrs': {
        'facebook': {
            'id': lambda _id: ('avatar_url', FACEBOOK_AVATAR_URL.format(_id)),
            'name': 'name',
            'link': 'link'
        },
        'google': {
            'picture': 'avatar_url',
            'name': 'name',
            'profile': 'link'
        },
        'googleplus': {
            'image': lambda img: ('avatar_url', img.get('url', DEFAULT_AVATAR_URL)),
            'displayName': 'name',
            'url': 'link'
        },
        'windows_live': {
            'avatar_url': 'avatar_url',
            'name': 'name',
            'link': 'link'
        },
        'twitter': {
            'profile_image_url': 'avatar_url',
            'screen_name': 'name',
            'link': 'link'
        },
        'linkedin': {
            'picture-url': 'avatar_url',
            'first-name': 'name',
            'public-profile-url': 'link'
        },
        'linkedin2': {
            'picture-url': 'avatar_url',
            'first-name': 'name',
            'public-profile-url': 'link'
        },
        'foursquare': {
            'photo': lambda photo: ('avatar_url', photo.get('prefix') + '100x100'\
                                    + photo.get('suffix')),
            'firstName': 'name',
            'contact': lambda contact: ('email', contact.get('email')),
            'id': lambda _id: ('link', FOURSQUARE_USER_LINK.format(_id))
        },
        'openid': {
            'id': lambda _id: ('avatar_url', DEFAULT_AVATAR_URL),
            'nickname': 'name',
            'email': 'link'
        }
    },
    'simple_auth_secrets': {
        'google': (GOOGLE_APP_ID, GOOGLE_APP_SECRET,
                   'https://www.googleapis.com/auth/userinfo.profile'),
        'googleplus': (GOOGLE_APP_ID, GOOGLE_APP_SECRET, 'profile'),
        'linkedin2': (LINKEDIN_KEY, LINKEDIN_SECRET, 'r_basicprofile'),
        'facebook': (FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, 'user_about_me'),
        'windows_live': (WL_CLIENT_ID, WL_CLIENT_SECRET, 'wl.signin'),
        'foursquare': (FOURSQUARE_CLIENT_ID, FOURSQUARE_CLIENT_SECRET,
                       'authorization_code'),

        # OAuth 1.0 providers don't have scopes
        'twitter': (TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET),
        'linkedin': (LINKEDIN_KEY, LINKEDIN_SECRET),
    },
    'simple_auth_optional_params': {
        # Provider auth init optional parameters
        # '<provider>': {'<parameter_name>': '<value>'}
        # ex. 'twitter' : {'force_login': True}
    },
    'csrf_token_name': '_csrf_token'

}
