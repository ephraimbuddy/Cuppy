from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.events import BeforeRender
from cuppy.models.users import User
from cuppy.utils.subscribers import add_renderer_globals
from pyramid.security import Everyone, Authenticated, ALL_PERMISSIONS, Allow
from pyramid_beaker import session_factory_from_settings

def session_factory(**settings):
    return session_factory_from_settings(settings)


SITE_ACL = [
    (Allow, Everyone, 'view'),
    (Allow,'group:viewer',('view')),
    (Allow, 'group:editor',('view','add','edit','state_change')),
    (Allow, 'group:owner',('view','add','edit','manage','state_change')),
    (Allow, 'group:admin', ('view','add','edit','manage','state_change',
                            'delete', 'cut', 'copy', 'paste', 'manage_permissions')),
    (Allow, 'group:superadmin', ALL_PERMISSIONS)

    ]
    

class RootFactory(object):

    def __init__(self, request):
        self.request = request

    def __acl__(self):
        return SITE_ACL
    

class CuppyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.id

    

def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        user = request.dbsession.query(User).get(user_id)
        return user
    return None


def groupfinder(userid,request):
    user = request.user
    if user is not None:
        return ["group:{}".format(g.name) for g in user.mygroups]
    return None


def includeme(config):
    settings = config.get_settings()
    session_factory = settings["cuppy.session_factory"][0](**settings)
    authn_policy = CuppyAuthenticationPolicy(
        settings['cuppy.auth_secret'],
        hashalg='sha512',callback=groupfinder)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_session_factory(session_factory)
    config.add_request_method(get_user, 'user', reify=True)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    cache = RootFactory.__acl__
    config.set_root_factory(RootFactory)
