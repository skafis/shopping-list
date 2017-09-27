
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField

from datetime import datetime


class ShoppingListEditForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired()
        ]
    )


class LoginForm(FlaskForm):
	username = StringField(
        'username', 
        validators=[
                DataRequired()
            ]
        )
	password = PasswordField(
        'password',
            validators=[
                DataRequired()
            ]
        )
