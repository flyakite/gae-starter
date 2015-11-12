Google App Engine Python Starter
================================

A [cookiecutter](https://github.com/audreyr/cookiecutter) template for [Google App Engine](https://cloud.google.com/appengine/) Python project.


Ingredients
-----------
+ [webapp2](http://webapp-improved.appspot.com/) Lightweight Python web framework compatible with GAE.
+ [Jinja2](http://jinja.pocoo.org/docs/) Modern and designer-friendly templating language for Python.
+ [NDB](http://developers.google.com/appengine/docs/python/ndb/) App Engine Datastore API.
+ [WTForms](http://wtforms.simplecodes.com/) A flexible forms validation and rendering library for Python.
+ [unittest](http://docs.python.org/library/unittest.html) The Python unit testing framework.
+ [webtest](http://webtest.pythonpaste.org/en/latest/index.html) WebTest helps you test your WSGI-based web applications.
+ [NoseGAE](https://github.com/Trii/NoseGAE) Nose plugin for Google App Engine testing.
+ [Fabric](http://www.fabfile.org) Suite of operations for executing local or remote shell commands.
+ [SimpleAuth](https://github.com/crhym3/simpleauth) Simple Authentication supporting OAuth and OpenID (Google, Facebook, ...)
+ [Bower](http://bower.io) A package manager for the web.
+ [Gulp](http://gulpjs.com) A streaming build tool built on Node.js.
+ [HTML5Boilerplate](http://html5boilerplate.com/) A professional front-end template.
+ [Modernizr](http://modernizr.com) A JavaScript library that detects HTML5 and CSS3 features in the user's browser.
+ [Sass](http://sass-lang.com) A scripting language that interpreted into CSS.
+ [LiveReload](https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei) A happy land where browsers don't need a Refresh button.
+ [jQuery](http://jquery.com) A fast, small, and feature-rich JavaScript library.
+ [Twitter Bootstrap](http://twitter.github.com/bootstrap/) Sleek, intuitive, and powerful front-end framework. (Optional)

[Demo](https://gae-starter2.appsppot.com)


Prerequisits
------------

1. Download and install [Google App Engine SDK](http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python).
1. Create a unique App ID in [Google Developers Console](https://console.developers.google.com/) and enable needed services and APIs.
1. Install Fabric
```
$ pip install Fabric
```

Get Started
-----------
Install latest cookiecutter and ruamel.yaml. (We need '_copy_without_render' function.)
``` 
$ pip install --upgrade git+https://github.com/audreyr/cookiecutter.git
$ pip install ruamel.yaml
```

Run cookiecutter to create your project.
```
$ cookiecutter gh:flyakite/gae-starter
```

Create virtual environment in project folder and install Python and Javascript packages.
```	 
$ cd <your_project>
$ virtualenv --python=python2.7 venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ npm install
$ bower install
```

Run Server
----------

Run Gulp tasks and start web server using Fabric command.
```	    
$ gulp
```
```	
$ fab start
```

Run Test
--------

```
$ fab test
```

Deploy to GAE
-------------

Run unittest and deploy to server.
```	
$ fab deploy
```

Social Login
------------

Please follow the instruction to apply and fill the secrets in config.py

1. Google
 * Register app in https://console.developers.google.com
 * Add https://<your_website>/auth/googleplus/callback to Redirect URIs
 * Enable Google Plus API https://console.developers.google.com/

1. Facebook
 * Register app in https://developers.facebook.com/apps
 * Add https://<your_website>/auth/facebook/callback to Redirect URLs

1. Linkedin
 * Register app in https://www.linkedin.com/secure/developer
 * Add http://<your_website>/auth/linkedin2/callback to Redriect URLs
 * Key/secret for both LinkedIn OAuth 1.0a and OAuth 2.0

1. Microsoft Live
 * Register app in http://go.microsoft.com/fwlink/?LinkID=144070
 * Add https://<your_website>/auth/windows_live/callback to Redirect URLs

1. Twitter
 * Register app in https://dev.twitter.com/apps
 * Add https://<your_website>/auth/twitter/callback to Redirect URLs

1. Foursquare
 * Register app in https://foursquare.com/developers/apps
 * Add https://<your_website>/auth/foursquare/callback to Redirect URLs
     
More info please refer to [SimpleAuth](https://github.com/crhym3/simpleauth)

