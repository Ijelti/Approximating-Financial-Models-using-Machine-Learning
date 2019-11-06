from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class FeaturesForm(FlaskForm):
    alpha = FloatField('Alpha', validators=[DataRequired()])
    beta = FloatField('Beta', validators=[DataRequired()])
    F = FloatField('F' , validators=[DataRequired()])
    nu = FloatField('nu' , validators=[DataRequired()])
    rho = FloatField('rho' , validators=[DataRequired()])
    T = FloatField('T' , validators=[DataRequired()])
    K = FloatField('K' , validators=[DataRequired()])
    submit1 = SubmitField('Polynomial regression')
    submit2 = SubmitField('Random forest')
    submit3 = SubmitField('Neural network')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')