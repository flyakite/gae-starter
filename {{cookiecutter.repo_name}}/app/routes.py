from webapp2 import Route

# some handlers import shortcuts are written in handlers/__init__.py
routes = [
    Route(r'/auth/<provider>', 'handlers.AuthHandler:_simple_auth', name='auth_login'),
    Route(r'/auth/<provider>/callback', 'handlers.AuthHandler:_auth_callback', name='auth_callback'),
    Route(r'/logout', 'handlers.AuthHandler:logout', name='logout'),
    Route(r'/', 'handlers.IndexHandler', name='index'),
]
