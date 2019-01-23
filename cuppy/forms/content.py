from datetime import timedelta

from wtforms import Form
from wtforms import StringField
from wtforms import validators
from wtforms import TextAreaField
from wtforms import BooleanField
from pyramid.settings import asbool

from ..utils.util import cuppy_settings

strip_filter = lambda x: x.strip() if x else None

class BaseForm(Form):
    class Meta:
        csrf = asbool(cuppy_settings('csrf'))
        csrf_class = cuppy_settings("csrf_class")[0]
        csrf_secret = cuppy_settings("csrf_secret")
        csrf_time_limit = timedelta(minutes=int(cuppy_settings('csrf_time_limit')))

    
class ContentForm(BaseForm):

    name = StringField("Name", validators=[validators.Length(max=200)],
                                filters = [strip_filter])

    title = StringField("Title", validators=[validators.InputRequired(),
                                            validators.Length(min=3, max=200)],
                                 filters = [strip_filter])

    slug = StringField("Slug", filters=[strip_filter])

    description = TextAreaField("Description", filters=[strip_filter])

    published = BooleanField(default="checked")

    in_navigation = BooleanField(default="checked")

