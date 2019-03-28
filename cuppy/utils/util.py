from itsdangerous import URLSafeTimedSerializer
import re
from unidecode import unidecode
import os.path
import os

from pyramid.settings import asbool
from pyramid.util import DottedNameResolver
from pyramid.threadlocal import get_current_registry
from pyramid.security import remember


# Define and compile static regexes
# The below codes are partly from Kotti CMS


FILENAME_REGEX = re.compile(r"^(.+)\.(\w{,4})$", re.U)
IGNORE_REGEX = re.compile(r"['\"]", re.U)
URL_DANGEROUS_CHARS_REGEX = re.compile(r"[!#$%&()*+,/:;<=>?@\\^{|}\[\]~`]+", re.U)
MULTIPLE_DASHES_REGEX = re.compile(r"\-+", re.U)
EXTRA_DASHES_REGEX = re.compile(r"(^\-+)|(\-+$)", re.U)
# Define static constraints
MAX_LENGTH = 200
MAX_URL_LENGTH = 50


def crop_name(base, maxLength=MAX_LENGTH):
    baseLength = len(base)

    index = baseLength
    while index > maxLength:
        index = base.rfind('-', 0, index)

    if index == -1 and baseLength > maxLength:
        base = base[:maxLength]

    elif index > 0:
        base = base[:index]

    return base


def url_normalizer(text, locale=None, max_length=MAX_URL_LENGTH):

    text = unidecode(text)

    # lowercase text
    base = text.lower()
    ext = ''

    m = FILENAME_REGEX.match(base)
    if m is not None:
        base = m.groups()[0]
        ext = m.groups()[1]

    base = base.replace(' ', '-')
    base = IGNORE_REGEX.sub('', base)
    base = URL_DANGEROUS_CHARS_REGEX.sub('-', base)
    base = EXTRA_DASHES_REGEX.sub('', base)
    base = MULTIPLE_DASHES_REGEX.sub('-', base)


    base = crop_name(base, maxLength=max_length)

    if ext != '':
        base = base + '.' + ext
    return base

def disambiguate_name(name):
    parts = name.split('-')
    if len(parts) > 1:
        try:
            index = int(parts[-1])
        except ValueError:
            parts.append('1')
        else:
            parts[-1] = ""+str(index + 1)

    else:
        parts.append('1')
    return '-'.join(parts)


def title_to_slug(title, blacklist=(),prepend=None, max_length=200):

    normalizer = cuppy_settings('url_normalizer')[0]
    name = normalizer(title, locale='en', max_length=max_length)
    if name not in blacklist:
        if prepend:
            return prepend+"/"+name
        return name
    while name in blacklist:
        name = disambiguate_name(name)
    if prepend:
        return prepend+"/"+name
    return name


def cuppy_remember(request, user, event='L'):
    from cuppy.models import AuthUserLog
    if asbool(cuppy_settings('log_logins')):
        ip_addr = request.client_addr
        record = AuthUserLog(user_id=user.id,
                             ip_addr=ip_addr,
                             event=event)
        request.dbsession.add(record)
        request.dbsession.flush()
        return remember(request, user.id)
    return remember(request, user.id)

def get_settings():
    return get_current_registry().settings

def cuppy_settings(key):
    """ Gets a cuppy setting if the key is set 
    """
    settings = get_settings()

    return settings.get('cuppy.%s' % key)
    

def get_module(package):
    """ Returns a module based on the string passed
    """
    resolver = DottedNameResolver(package.split('.', 1)[0])
    return resolver.resolve(package)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(cuppy_settings('email_secret'))
    return serializer.dumps(email, salt=cuppy_settings('email_secret_password'))


def confirm_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(cuppy_settings('email_secret'))
    ex= cuppy_settings("confirm_token_expiration")
    if ex:
        expiration = ex
    try:
        email = serializer.loads(
            token,
            salt=cuppy_settings('email_secret_password'),
            max_age=expiration
        )
    except:
        return False
    return email



    