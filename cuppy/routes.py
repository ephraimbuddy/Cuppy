from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import Allow

from .models.users import User
from .security import SITE_ACL


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('signup', '/signup')
    config.add_route('signin','/signin')
    config.add_route('signout', '/signout')
    config.add_route('email_activate', '/activate/{token}')
    config.add_route('forgot_password', '/passforgot')
    config.add_route('reset_password', '/reset/{token}')
    config.add_route('send_confirmation_email', '/send_email_confirmation')
    

def userfactory(request):
    username = request.matchdict['username']
    user = User.get_by_username(username)
    
    if user is None:
        raise HTTPNotFound()
    return UserResource(user)
    

class UserResource(object):
    def __init__(self,user):
       self.user = user

    def __acl__(self):
        acl = SITE_ACL
        acl.append((Allow, str(self.user.id),('edit')))
        return acl