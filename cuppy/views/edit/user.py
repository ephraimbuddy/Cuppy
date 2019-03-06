from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import forget

from cuppy.utils.util import cuppy_remember
from cuppy.forms.userform import GroupForm
from cuppy.forms.userform import SignupForm
from cuppy.forms.userform import LoginForm
from cuppy.models import Groups
from cuppy.models import ObjectInsert
from cuppy.models import ObjectUpdate
from cuppy.models import ObjectDelete
from cuppy.models import User

@view_config(route_name="list_group", renderer = "cuppy:templates/derived/group/list_group.mako")
def groups(request):
    groups = request.dbsession.query(Groups).all()
    return dict(groups = groups)


@view_config(route_name="add_group", renderer="cuppy:templates/derived/group/add.mako")
def addgroup(request):
    form = GroupForm(request.POST, meta={'csrf_context':request.session})
    if request.POST and form.validate():
        appstruct = form.data
        appstruct.pop('csrf_token')
        group = Groups(**appstruct)
        request.dbsession.add(group)
        return HTTPFound(location = request.route_url('list_group'))
    return dict(form=form, action_url= request.route_url('add_group'))


@view_config(route_name="edit_group", renderer="cuppy:templates/derived/group/edit.mako")
def editgroup(request):
    id_ = request.matchdict['id']
    group = request.dbsession.query(Groups).get(id_)
    if not group:
        return HTTPNotFound()
    form = GroupForm(request.POST, meta={'csrf_context':request.session}, obj = group)
    if request.POST and form.validate():
        appstruct = form.data
        appstruct.pop('csrf_token')
        for k, v in appstruct.items():
            setattr(group, k, v)
        request.dbsession.merge(group)
        return HTTPFound(location = request.route_url('list_group'))
    
    return dict(form=form, action_url= request.route_url('edit_group', id=id_), group=group)


@view_config(route_name="delete_group")
def delete_group(request):
    id_ = request.matchdict['id']
    group = request.dbsession.query(Groups).get(id_)
    if not group:
        return HTTPNotFound()
    request.dbsession.delete(group)
    return HTTPFound(location=request.route_url('list_group'))
    

@view_config(route_name="signup", renderer='cuppy:templates/derived/account/signup.mako')
def reg(request):
    form = SignupForm(request.POST, meta={'csrf_context':request.session})
    action_url = request.route_url('signup')
    if request.POST and form.validate():
        email = User.get_by_email(form.email.data)
        if email:
            request.session.flash("info; This email is already in use")
            return HTTPFound(location = request.route_url('home'))
        username = User.get_by_username(form.username.data)
        if username:
            request.session.flash("info; This username is not available")
            return HTTPFound(location = request.route_url('home'))
        user = User(first_name=form.first_name.data,
                    email = form.email.data,
                    last_name = form.last_name.data,
                    username=form.username.data)
        user.set_password(form.password.data)
        request.dbsession.add(user)
        headers = cuppy_remember(request, user, event="R")
        #if cuppy_settings("verify_email"):
            #send email
         #   pass
        request.session.flash('success; New user added')
        return HTTPFound(location=request.route_url('home'), headers=headers)
    return dict(form=form, action_url = action_url)


@view_config(route_name='signin', renderer='cuppy:templates/derived/account/signin.mako')
@forbidden_view_config(renderer='cuppy:templates/derived/account/signin.mako')
def sign_in(request):
    if request.user:
        request.session.flash("info; You're already signed in")
        return HTTPFound(location=request.route_url('home'))
    form = LoginForm(request.POST, meta={'csrf_context': request.session})
    login_url = request.route_url('signin')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    error_cls = ''
    if request.POST and form.validate():
        email = form.email.data
        user = User.get_by_email(email)
        if user and user.check_password(form.password.data):
            headers = cuppy_remember(request, user)
            return HTTPFound(location=came_from, headers=headers)

        message = 'Failed login, Please try again'
        error_cls = 'has-error'
        return dict(form=form, message=message, error_cls=error_cls, came_from=came_from, action_url=login_url)
    return dict(form=form, message=message, came_from=came_from, error_cls=error_cls, action_url=login_url)


@view_config(route_name="signout", renderer="string")
def signout(request):
    headers = forget(request)
    request.session.invalidate()
    return HTTPFound(location='/', headers=headers)

