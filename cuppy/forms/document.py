from wtforms import validators
from wtforms import TextAreaField

from cuppy.forms.content import ContentForm



class AddDocument(ContentForm):
    
    body = TextAreaField("Body", validators=[validators.InputRequired(),
                                            validators.Length(min=10)] )

