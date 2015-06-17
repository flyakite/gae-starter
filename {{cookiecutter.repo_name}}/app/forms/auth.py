from wtforms import Form, TextField, PasswordField, validators


class SignupForm(Form):

    """
    WTForm Fields:
    https://wtforms.readthedocs.org/en/latest/fields.html

    We can use PasswordField(input type=password) for password field
    if we want to hide the password from the user.

    """
    username = TextField('Username',
                         [validators.Required(),
                          validators.Length(min=4),
                          validators.Regexp(r'[a-zA-Z0-9]+',
                                            message="Username must not contain special characters.")])
    password = TextField('Password',
                         [validators.Required(),
                          validators.Length(min=6)])
