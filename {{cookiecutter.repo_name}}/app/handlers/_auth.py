# *-* coding: utf-8 *-*

import logging
from models.user import User
from libs.decorators import csrf
from forms.auth import SignupForm
from base import AuthHandler


class ProfileHandler(AuthHandler):

    def get(self):
        logging.info('user_id {0}'.format(self.user_id))
        return self.render('profile')


class SignupHandler(AuthHandler):

    @csrf
    def post(self):
        form = SignupForm(self.request.POST)
        error_message = ""
        if form.validate():
            auth_id = 'own:' + form.username.data
            ok, user = User.create_user(auth_id, username=form.username.data, password_raw=form.password.data)
            if ok:
                self.login_user(user)
                return self.redirect(self.uri_for('profile'))
            else:
                return self.redirect('/', error_message='Sign Up Error')

    def get(self):
        return self.redirect('/')
