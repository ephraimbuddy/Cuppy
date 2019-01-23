from cuppy.forms.content import BaseForm, strip_filter
from wtforms import StringField, PasswordField ,validators, ValidationError, FileField, TextAreaField



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
    email = StringField("Email", validators=[validators.InputRequired(),
                    validators.Email(message="invalid email address")], filters=[strip_filter])
    password = PasswordField("Password", validators=[validators.InputRequired(),
                password_validator,validators.Length(min=6),validators.EqualTo("confirm", message="Password must match")])
    confirm = PasswordField("Repeat Password", validators=[validators.InputRequired()])
     
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