from functools import wraps
from config import config


class CSRFException(Exception):
    pass


def csrf(handler):
    @wraps(handler)
    def inner(self, *args, **kwargs):
        if self.request.method in ["POST", "PUT", "DELETE"]:
            ctn = config['csrf_token_name']
            token = self.session.get(ctn)
            if not token:
                raise CSRFException("CSRF token not in session.")
                self.abort(403)
            elif (token != self.request.get(ctn) and
                  token != self.request.headers.get(ctn)):
                raise CSRFException("CSRF token doesn't match.")
                self.abort(403)
        return handler(self, *args, **kwargs)
    return inner
