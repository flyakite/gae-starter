#!/usr/bin/env python

__author__ = "{{cookiecutter.author_name}} <{{cookiecutter.email}}>"
__version__ = "{{cookiecutter.version}}"

import os
import sys
import webapp2
sys.path.append(os.path.join(os.path.dirname(__file__) + '/libs'))

from config import config
from routes import routes

app = webapp2.WSGIApplication(routes,
                              debug=os.environ['SERVER_SOFTWARE'].startswith('Dev'),
                              config=config)
