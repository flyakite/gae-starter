import os
from fabric.api import local, lcd


def start(clear_datastore=""):
    """
    start web server
    """

    if clear_datastore == "clear":
        local("dev_appserver.py ./app/ --host 127.0.0.1 --port {{cookiecutter.local_web_server_port}} --clear_datastore --skip_sdk_update_check")
    else:
        local("dev_appserver.py ./app/ --host 127.0.0.1 --port {{cookiecutter.local_web_server_port}} --skip_sdk_update_check")


def gulp(task="default"):
    """
    start gulp
    """
    local("gulp %s" % task)


def deploy(no_cookie=""):
    """
    deploy app to GAE server
    """
    if no_cookie:
        local("appcfg.py update ./app/ --no_cookies")
    else:
        local("appcfg.py update ./app/")


def rollback():
    """
    rollback last deploy
    """
    local("appcfg.py rollback ./app/")


def test():
    """
    fab test:/path/to/google_appengine_sdk
    """

    with lcd("app/"):
        os.environ['SERVER_SOFTWARE'] = 'Development'
        local("nosetests --with-gae")
