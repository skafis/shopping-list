'''
This file is responsible for handling all the forms
'''
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from wtforms.validators import DataRequired

class ShoppingListEditForm(FlaskForm):
    '''
    This class handles the forms for
    adding shopping list and editing it
    '''
    title = StringField(
        'Title',
        validators=[
            DataRequired()
        ]
    )


class LoginForm(FlaskForm):
    '''
    The class handling the login form
    '''
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    '''
    The class handles the signup forms
    '''
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('New password', [validators.DataRequired(),
                                              validators.EqualTo('confirm',
                                                                 message='Password must match')])
    confirm = PasswordField('Repeat Password')
    