from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import forget

from cuppy.forms.userform import GroupForm
from cuppy.forms.userform import SignupForm
from cuppy.forms.userform import LoginForm
from cuppy.forms.userform import ChangePasswordForm
from cuppy.forms.userform import ResetPasswordForm
from cuppy.forms.userform import ChangePasswordForm
from cuppy.forms.userform import ChangeEmailForm
from cuppy.forms.userform import UserEditForm
from cuppy.models import Groups
from cuppy.models import ObjectInsert
from cuppy.models import ObjectUpdate
from cuppy.models import ObjectDelete
from cuppy.models import User
from cuppy.utils.util import generate_confirmation_token
from cuppy.utils.util import confirm_token
from cuppy.utils.util import cuppy_settings
from cuppy.utils.util import cuppy_remember
from cuppy.mailing import welcome, email_forgot, user_regmail, confirm_email


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
    

@view_config(route_name="users", renderer="cuppy:templates/derived/account/users.mako")
def users(request):
    users = request.dbsession.query(User).all()
    return dict(users = users)


@view_config(route_name='admin_edit_user', renderer = "cuppy:templates/derived/account/admin_edit_user.mako")
def admin_edit_users(request):
    id_ = request.matchdict['id']
    user = User.get_by_id(id_)
    if not user:
        return HTTPNotFound()
    groups = Groups.get_all()
    form = UserEditForm(request.POST, meta={'csrf_context': request.session}, obj=user)
    if request.POST and form.validate():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.about = form.about.data
        if user.email != form.email.data:
            user_is_available = User.get_by_email(form.email.data)
            if not user_is_available:
                user.email == form.email.data 
        request.dbsession.merge(user)
        return HTTPFound(location = request.route_url('users'))
    return dict(user=user, form=form, groups=groups)


@view_config(route_name="add_to_group")
def make_admin(request):
    id_ = request.matchdict['user_id']
    user = User.get_by_id(id_)
    name = request.matchdict['name']
    group = request.dbsession.query(Groups).filter(Groups.name==name).first()
    if user and group:
        user.mygroups.append(group)
        request.session.flash('success; %s added to group %s'%(user.fullname,group.name))
        return HTTPFound(location=request.route_url('admin_edit_user',id=user.id))
    request.session.flash('danger; Not successfull')
    return HTTPFound(location=request.route_url('admin_edit_user', id=user.id))


@view_config(route_name="remove_from_group")
def remove_from_group(request):
    id_ = request.matchdict['user_id']
    user = User.get_by_id(id_)
    name = request.matchdict['name']
    group = request.dbsession.query(Groups).filter(Groups.name==name).first()
    if user and group:
        if group in user.mygroups:
            user.mygroups.remove(group)
            request.session.flash('success; %s removed from group %s'%(user.fullname,group.name))
        return HTTPFound(location=request.route_url('admin_edit_user',id=user.id))
    request.session.flash('danger; Not successfull')
    return HTTPFound(location=request.route_url('admin_edit_user', id=user.id))


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
        if cuppy_settings("verify_email"):
            token = generate_confirmation_token(user.email)
            #Send email here
        request.session.flash('success; Registration successful')
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


@view_config(route_name="email_activate")
def verify_email(request):
    title = "Email Confirmation"
    token = request.matchdict.get('token')
    try:
        email = confirm_token(token)
    except:
        message = 'Error verifying message: email expired'
        request.session.flash('danger;%s' % message)
        return HTTPFound(location='/')
    user = User.get_by_email(email)
    
    if user.email_verified:
        request.session.flash('success;Account already confirmed. Please login.', 'success')
        return HTTPFound(location='/')
    else:
        user.email_verified = True
        welcome(request, user)
        request.dbsession.merge(user)
        request.dbsession.flush()
        message = 'Your email is now confirmed. Thank you for joining us'
        request.session.flash('success;%s' % message)
        return HTTPFound(location='/')


@view_config(route_name="send_confirmation_email", permission='post')
def send_email_confirm(request):
    token = generate_confirmation_token(request.user.email)
    confirm_email(request, request.user, request.user.email, token)
    request.session.flash("success; An email confirmation link has been sent to your mailbox")
    return HTTPFound(location=request.route_url('dashboard-index'))


@view_config(route_name="forgot_password", renderer="cuppy:templates/derived/account/forgot.mako")
def passforgot(request):
    form = ChangeEmailForm(request.POST, meta={'csrf_context': request.session})
    if request.method=="POST" and form.validate():
        user = User.get_by_email(form.email.data)
        if user:
            token = generate_confirmation_token(user.email)
            email_forgot(request, user, user.email, token)
            request.session.flash('info; We have sent you a link to reset your password, please check your email')
            return HTTPFound(location=request.route_url('home'))
        request.session.flash("warning; We can't find an account with such email here")
        return HTTPFound(location=request.route_url('home'))
    return dict(form=form, title="Forgot Password")


@view_config(route_name="reset_password", renderer="cuppy:templates/derived/account/resetpassword.mako")
def restpass(request):
    title="Reset password"
    token = request.matchdict.get('token')
    try:
        email = confirm_token(token)
    except:
        message = 'Error verifying message: email expired'
        request.session.flash('danger;%s' % message)
        return HTTPFound(location='/')
    form = ResetPasswordForm(request.POST, meta={'csrf_context': request.session})
    if request.POST and form.validate():
        user = User.get_by_email(email)
        user.set_password(form.password.data)
        request.dbsession.merge(user)
        request.dbsession.flush()
        request.session.flash('success; Password Changed. Please log in')
        return HTTPFound(location=request.route_url('home'))
    action_url = request.route_url("reset_password", token=token)
    return {'title': title,
            'form': form, 'action_url': action_url}

