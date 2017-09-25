
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

    year = IntegerField(
        'Year',
        validators=[
            Optional(),
            NumberRange(min=1887, max=datetime.now().year)
        ]
    )

class LoginForm(FlaskForm):
	username = StringField()
	password = PasswordField()
