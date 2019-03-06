from datetime import timedelta

from wtforms import Form, Field
from wtforms import StringField
from wtforms import validators
from wtforms import TextAreaField
from wtforms import RadioField
from wtforms import BooleanField
from wtforms import DateTimeField
from wtforms.widgets import TextInput
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
    

class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []


class BetterTagListField(TagListField):
    def __init__(self, label='', validators=None, remove_duplicates=True, **kwargs):
        super(BetterTagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def process_formdata(self, valuelist):
        super(BetterTagListField, self).process_formdata(valuelist)
        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


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
    
    tags = BetterTagListField("Tags", description="Enter a comma separated list of tags")
    



class AddDocument(ContentForm):
    
    body = TextAreaField("Body", validators=[validators.InputRequired(),
                                            validators.Length(min=10)] )