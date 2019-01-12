from itsdangerous import URLSafeTimedSerializer
from pyramid.settings import asbool
from pyramid.util import DottedNameResolver
from cuppy.models.users import AuthUserLog
from pyramid.threadlocal import get_current_registry
from pyramid.security import remember


def cuppy_settings(key=None, default=None):
    """ Gets a cuppy setting if the key is set.
        If no key is set, returns all the cuppy settings.

    """
    settings = get_current_registry().settings

    if key:
        return settings.get('cuppy.%s' % key, default)
    else:
        cuppy_settings = []
        for k, v in settings.items():
            if k.startswith('cuppy.'):
                cuppy_settings.append({k.split('.')[1]: v})
        return cuppy_settings


def get_module(package):
    """ Returns a module based on the string passed
    """
    resolver = DottedNameResolver(package.split('.', 1)[0])
    return resolver.resolve(package)


def cuppy_remember(request, user, event='L'):
    if asbool(cuppy_settings('log_logins')):
        if cuppy_settings('log_login_header'):
            ip_addr = request.environ.get(cuppy_settings('log_login_header'),
                                          u'invalid value - cuppy.log_login_header')
        else:
            ip_addr = request.client_addr
        record = AuthUserLog(user_id=user.id,
                             ip_addr=ip_addr,
                             event=event)
        request.dbsession.add(record)
        request.dbsession.flush()
        return remember(request, user.id)
    return remember(request, user.id)

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
