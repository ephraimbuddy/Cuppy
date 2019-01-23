import pytz
from .util import cuppy_settings


timezone = pytz.timezone(cuppy_settings('timezone'))
NUMBER = '123456789'