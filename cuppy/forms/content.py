from datetime import timedelta

from wtforms import Form
from wtforms import StringField
from wtforms import validators
from wtforms import TextAreaField
from wtforms import RadioField
from wtforms import BooleanField
from wtforms import DateTimeField
from wtforms.csrf.session import SessionCSRF

from pyramid.settings import asbool

from ..utils.util import cuppy_settings

strip_filter = lambda x: x.strip() if x else None

class BaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = cuppy_settings("csrf_secret_key")
        csrf_time_limit = timedelta(minutes=20)
    

    
class ContentForm(BaseForm):

    # Meta
    meta_title = StringField("Meta Title", filters = [strip_filter], description="Optional title to be used in the HTML title tag. If left blank, the main title field will be used.")

    slug = StringField("Slug", filters=[strip_filter], description="Leave blank to have the URL auto-generated from the title.")

    description = TextAreaField("Meta Description", filters=[strip_filter],
                                description = "Leave blank to have the description auto-generated from the content.")
    
    # Content
    title = StringField("Title", validators=[validators.InputRequired(),
                                            validators.Length(min=3, max=200)],
                                 filters = [strip_filter])
    creation_date = DateTimeField("Creation Date",
                                description = "Leave blank to have the creation date auto-generated. format=> Y-m-d H:m:s")

    status = RadioField("Status", choices = [('draft', 'Draft'), ('published', 'Published')], default="published")

    in_menu = BooleanField("In menu", default='checked')
    
    



class AddDocument(ContentForm):
    
    body = TextAreaField("Body", validators=[validators.InputRequired(),
                                            validators.Length(min=10)] )