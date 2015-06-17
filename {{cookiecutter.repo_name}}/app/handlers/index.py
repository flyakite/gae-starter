# *-* coding: utf-8 *-*

import logging
from models.user import User
from libs.decorators import csrf
from forms.auth import SignupForm
from base import AuthHandler


class IndexHandler(AuthHandler):

    def get(self):
        form = SignupForm()
        return self.render('index', form=form)

    @csrf
    def post(self):
        """
        An example how to use 'csrf' decorator.
        We can also use CSRF within WTForms.
        """
        form = SignupForm(self.request.POST)
        error_message = ""
        if form.validate() and not self.auth.get_user_by_session():
            auth_id = 'own:{0}'.format(form.username.data)
            ok, new_user = User.create_user(auth_id, username=form.username.data, password_raw=form.password.data)
            if ok:
                logging.debug('New User Created')
                self.login_user(new_user)
            else:
                error_message = "Username dulplicated."

        return self.render('index', form=form, error_message=error_message)
