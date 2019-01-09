from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.events import BeforeRender
from cuppy.models.users import User, RootFactory
from cuppy.utils.subscribers import add_renderer_globals


class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.id


def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        user = request.dbsession.query(User).get(user_id)
        return user


def get_root_user(request):
    user = request.dbsession.query(User).get(1)
    return user


def groupfinder(userid,request):
    user = request.user
    if user is not None:
        return [g.name for g in user.mygroups]
    return None


def includeme(config):
    settings = config.get_settings()
    authn_policy = MyAuthenticationPolicy(
        settings['auth.secret'],
        hashalg='sha512',callback=groupfinder)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_request_method(get_user, 'user', reify=True)
    config.add_request_method(get_root_user, 'root_user', reify=True)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    cache = RootFactory.__acl__
    config.set_root_factory(RootFactory)
