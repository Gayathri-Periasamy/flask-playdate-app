from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flaskplaydate.models import User
from datetime import datetime,date,time


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(),Length(min=2, max=20)]) 
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

# validation format for fields - for reference
    #def validate_field(self,field):
     #   if True:
      #      raise ValidationError('Validation message')

    def validate_username(self,username):
       user = User.query.filter_by(username=username.data).first()
       if user:
          raise ValidationError('Username already exists. Please choose a different one.')
       
    def validate_email(self,email):
       user = User.query.filter_by(email=email.data).first()
       if user:
          raise ValidationError('Email already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember= BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(),Length(min=2, max=20)]) 
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
       if username.data != current_user.username:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
       
    def validate_email(self,email):
       if email.data != current_user.email:
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose a different one.')
    
       
class PlaydateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    city = StringField ('Location (City/Area)', validators=[DataRequired(), Length(min=3, max=70), Regexp(
       r"^(?=.*[A-Za-z])[A-Za-z0-9 ,.'-]{3,100}$", message="Location must contain only letters, numbers, spaces, and common punctuation."
    )])
    date=DateField('Playdate Date', validators=[DataRequired()])
    time=TimeField('Playdate Time', validators=[DataRequired()])
    submit = SubmitField('Post Playdate')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        
        today= date.today()
        if self.date.data < today:
            self.date.errors.append("Date cannot be in the past")
            return False
    
        event_dt = datetime.combine(self.date.data,self.time.data)
        now=datetime.now()
        if event_dt <= now:
            self.time.errors.append("Time must be in the future")
            return False
        return True

    