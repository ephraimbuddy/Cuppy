__author__ = 'ephraim'
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta
from wtforms import Form


strip_filter = lambda x: x.strip() if x else None

class BaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'\xf4?\xf9\xd6R\x00<\xb9\x04\xa6*\xfb\xb3\x16\xeb'
        csrf_time_limit = timedelta(minutes=20)
