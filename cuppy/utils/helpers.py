from cuppy.forms.userform import SignupForm,AddProfilePicture
from webhelpers2.html.tags import *
from webhelpers2.text import *
from webhelpers2.containers import *
from pyramid.renderers import render
from pyramid.security import has_permission
from webhelpers2.html import literal
from webhelpers2.date import time_ago_in_words
from cuppy.utils.url_normalizer import urlify_name
import datetime
__author__ = 'ephraim'

from .url_normalizer import urlify_name

def posted_date(date_v):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    if date_v.date() == today:
        return time_ago_in_words(date_v, granularity="minute") + " ago"
    elif date_v.date() == yesterday:
        return date_v.strftime("Yesterday at  %I:%M%p").lower()
    else:
        return date_v.strftime("%a %b %d, %Y")


def signup(request):
    form = SignupForm(request.POST,meta={'csrf_context': request.session})
    return render('cuppy:templates/base/sn.mako',dict(form=form),request=request)


def forgot(request):
    form = ChangeEmailForm(request.POST, meta={'csrf_context':request.session})
    return render('cuppy:templates/base/forgot.mako',dict(form=form), request=request)


def picture_upload(request):
    form = AddProfilePicture(request.POST, meta={'csrf_context': request.session}, obj=request.user)
    return render('cuppy:templates/account/picture_upload.mako', dict(form=form), request=request)

def cover_picture_upload(request):
    form = AddProfilePicture(request.POST, meta={'csrf_context': request.session}, obj=request.user)
    return render('cuppy:templates/account/cover_picture_upload.mako', dict(form=form), request=request)
