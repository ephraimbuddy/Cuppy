from datetime import datetime
from webhelpers2.text import remove_formatting, truncate
from pyramid.events import subscriber

from cuppy.models import User
from cuppy.utils.util import title_to_slug
from cuppy.utils.util import disambiguate_name

import logging
log = logging.getLogger(__name__)

class ObjectEvent(object):
    def __init__(self, obj, request, parent_id=None):
        self.request = request
        self.object = obj
        self.parent_id = parent_id


class ObjectInsert(ObjectEvent):
    """This event is emitted when an object is inserted into the DB."""


class ObjectUpdate(ObjectEvent):
    """This event is emitted when an object in the DB is updated."""


class ObjectDelete(ObjectEvent):
    """This event is emitted when an object is deleted from the DB."""



class UserEvent(object):
    def __init__(self, request, user):
        self.request = request
        self.user = user


class UserInsert(UserEvent):
    """This event is emitted when a user is added into the DB"""


class UserUpdate(UserEvent):
    """ This event is emitted when a user in the DB is updated"""

    
class UserDeleted(UserEvent):
    """ This event is emitted when a user is deactivated or deleted"""
    

@subscriber(ObjectInsert)
def set_creation_date(event):
    """Set ``creation_date`` of the object that triggered the event.

    :param event: event that trigerred this handler.
    :type event: :class:`ObjectInsert`
    """
    log.debug("setting creation date")
    obj = event.object
    obj.creation_date = obj.modification_date = datetime.now()
    


@subscriber(ObjectInsert)
def set_meta(event):
    """Set ``meta_title``, ``meta_description`` and ``slug`` of the Content object.

    :param event: event that trigerred this handler.
    :type event: :class:`ObjectInsert`
    """
    log.debug('setting meta')
    parent_id = event.parent_id
    obj = event.object
    if parent_id:
        obj.parent_id = parent_id
    if obj.meta_title is None:
        obj.meta_title = obj.title
    if obj.description is None:
        ends = ("</p>", "<br />", "<br/>", "<br>", "</ul>",
                "\n", ". ", "! ", "? ")
        for end in ends:
            pos = obj.body.lower().find(end)
            if pos >-1:
                obj.description = remove_formatting(obj.body[:pos])
        #else:
          #  obj.description = remove_formatting(truncate(obj.body,200,indicator='',whole_word = True))
    if obj.slug is None:
        obj.slug = obj.generate_unique_slug(parent_id)
    else:
        # If we have slug, make it unique
        if obj.parent_id:
           obj.slug =title_to_slug(obj.slug, obj.keys(parent_id), obj.parent.get_slug()) 
        obj.slug =title_to_slug(obj.slug, obj.keys())


@subscriber(ObjectInsert)
def set_ownership(event):
    """Set ``user_id`` of the content object.

    :param event: event that trigerred this handler.
    :type event: :class:`ObjectInsert`
    """
    obj = event.object
    request =event.request
    user = request.user
    if obj.user is None:
        obj.user = user


@subscriber(ObjectUpdate)
def set_modification_date(event):
    """Set ``modification_date`` of the content object.

    :param event: event that trigerred this handler.
    :type event: :class:`ObjectUpdate`
    """
    obj = event.object
    obj.modification_date = datetime.now()


# User related events

@subscriber(UserInsert)
def set_username(event):
    """Generate unique username of the user if no username set in the form"""
    request = event.request
    usernames = [i.username for i in request.dbsession.query(User).all()]
    user = event.user
    if user.username is None:
        username = user.email.split('@')[0]
        if username not in usernames:
            user.username=username
        else:
            while username in usernames:
                username = disambiguate_name(username)
            user.username = username


@subscriber(UserInsert)
def set_join_date(event):
    """Set the date the user registered on the site"""
    user = event.user
    user.join_date = datetime.now()