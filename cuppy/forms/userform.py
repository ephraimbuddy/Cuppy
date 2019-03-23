import re
from cuppy.forms.content import BaseForm, strip_filter
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators
from wtforms import ValidationError
from wtforms import FileField
from wtforms import TextAreaField
from wtforms import SelectMultipleField
from cuppy.models.users import Groups




class UserEditForm(BaseForm):

    first_name = StringField("First name",validators=[validators.InputRequired(),
                    validators.Length(min=3, max=100)], filters=[strip_filter])
    last_name = StringField("Last name",validators=[validators.InputRequired(),
                    validators.Length(min=3, max=100)], filters=[strip_filter])
    username = StringField("Username", validators = [validators.Regexp("\w+$", message="Username can only contain letters,numbers and underscores")], 
        filters=[strip_filter])
    email = StringField("Email", validators=[validators.InputRequired(),
                    validators.Email(message="invalid email address")], filters=[strip_filter])
    
    about = TextAreaField("About", filters= [strip_filter])


class GroupForm(BaseForm):
    name = StringField("Name", validators = [validators.InputRequired(),
            validators.Length(min=3, max=100)], filters=[strip_filter])
    description = StringField("Description")


class ChangeEmailForm(BaseForm):
    email = StringField("Email", validators=[validators.InputRequired(),
                                   validators.Email(message="invalid email address")], filters=[strip_filter])
                                   
def password_validator(form, field):
    if len(field.data)<6:
        raise ValidationError("Your password is too short, add more variety")
    if field.data==u'123456':
        raise ValidationError("Please make your password more hard to guess")
    elif field.data==u'abcdef':
        raise ValidationError("Your password will be easy to guess, add more variety")
    elif field.data==u'qwerty':
        raise ValidationError("Such passwords are known to be easy to guess, add more variety")

class SignupForm(BaseForm):
    first_name = StringField("First name",validators=[validators.InputRequired(),
                    validators.Length(min=3, max=100)], filters=[strip_filter])
    last_name = StringField("Last name",validators=[validators.InputRequired(),
                    validators.Length(min=3, max=100)], filters=[strip_filter])
    username = StringField("Username", validators = [validators.Regexp("\w+$", message="Username can only contain letters,numbers and underscores")], 
        filters=[strip_filter])
    email = StringField("Email", validators=[validators.InputRequired(),
                    validators.Email(message="invalid email address")], filters=[strip_filter])
    password = PasswordField("Password", validators=[validators.InputRequired(),
                password_validator,validators.Length(min=6),validators.EqualTo("confirm", message="Password must match")])
    confirm = PasswordField("Repeat Password", validators=[validators.InputRequired()])


class ResetPasswordForm(BaseForm):
    password = PasswordField("Password", validators=[validators.InputRequired(),
                    password_validator,validators.Length(min=6),validators.EqualTo("confirm_password", message="Password must match")])
    confirm_password = PasswordField("Repeat Password", validators=[validators.InputRequired()])
    

class LoginForm(BaseForm):
    email = StringField("Email", validators=[validators.InputRequired(),
                    validators.Email(message="invalid email address")], filters=[strip_filter])
    password = PasswordField("Password", validators=[validators.InputRequired()])
     
class NameEditForm(BaseForm):
    first_name = StringField("First name", validators=[validators.InputRequired()])
    last_name = StringField("Last name", validators=[validators.InputRequired()])
    


class ChangePasswordForm(BaseForm):
    old_password = PasswordField("old Password", validators=[validators.InputRequired()])
    password = PasswordField("Password", validators=[validators.InputRequired(),password_validator,validators.Length(min=6),validators.EqualTo("confirm", message="Password must match")])
    confirm = PasswordField("Repeat Password", validators=[validators.InputRequired()])

class AddProfilePicture(BaseForm):
    picture = FileField("Picture")

class AddAboutForm(BaseForm):
    about = TextAreaField('About', validators=[validators.InputRequired()], filters=[strip_filter])