from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import InputRequired, Length, DataRequired, Email


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=3, max=10)])
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])

    submit = SubmitField('Sign Up')
