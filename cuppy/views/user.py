from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from cuppy.forms.userform import SignupForm
from cuppy.models.users import User
from cuppy.utils.util import buddy_remember, generate_confirmation_token
from cuppy.mailing.account import user_regmail

@view_config(route_name="signup", renderer="buddy:templates/derived/account/signup.mako")
def signup(request):
    msg=''
    if request.user:
        request.session.flash("info; You are already signed in")
        return HTTPFound(location='/')
    form = SignupForm(request.POST, meta={'csrf_context': request.session})
    if request.method == 'POST' and form.validate():
        email_exists = User.get_by_email(form.email.data)
        if email_exists:
            msg = "An account with this email address, already exists"
            return dict(form=form, msg=msg, title="Account Registration")
        user = User(first_name=form.first_name.data, 
                    last_name=form.last_name.data,
                    username = form.username.data,
                    email = form.email.data
                    )
        user.set_password(form.password.data)
        request.dbsession.add(user)
        headers = buddy_remember(request, user, event='R')
        token = generate_confirmation_token(user.email)
        user_regmail(request, user, user.email, token)
        
        return HTTPFound(location=request.route_url('home'), headers=headers)

    return dict(form=form, msg=msg, title="Account Registration")
