from itsdangerous import URLSafeTimedSerializer
from pyramid.settings import asbool
from pyramid.util import DottedNameResolver
from codepython.models.users import AuthUserLog
from pyramid.threadlocal import get_current_registry
from pyramid.security import remember


def buddy_settings(key=None, default=None):
    """ Gets a buddy setting if the key is set.
        If no key is set, returns all the buddy settings.

        Some settings have issue with a Nonetype value error,
        you can set the default to fix this issue.
    """
    settings = get_current_registry().settings

    if key:
        return settings.get('buddy.%s' % key, default)
    else:
        buddy_settings = []
        for k, v in settings.items():
            if k.startswith('buddy.'):
                buddy_settings.append({k.split('.')[1]: v})
        return buddy_settings


def get_module(package):
    """ Returns a module based on the string passed
    """
    resolver = DottedNameResolver(package.split('.', 1)[0])
    return resolver.resolve(package)


def buddy_remember(request, user, event='L'):
    if asbool(buddy_settings('log_logins')):
        if buddy_settings('log_login_header'):
            ip_addr = request.environ.get(buddy_settings('log_login_header'),
                                          u'invalid value - buddy.log_login_header')
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
    serializer = URLSafeTimedSerializer(buddy_settings('email_secret'))
    return serializer.dumps(email, salt=buddy_settings('email_secret_password'))


def confirm_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(buddy_settings('email_secret'))
    try:
        email = serializer.loads(
            token,
            salt=buddy_settings('email_secret_password'),
            max_age=expiration
        )
    except:
        return False
    return email
