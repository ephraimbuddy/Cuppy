from datetime import datetime
from pyramid.events import subscriber

from cuppy.utils.util import title_to_slug

class ObjectEvent(object):
    def __init__(self, obj, request):
        self.request = request
        self.object = obj


class ObjectInsert(ObjectEvent):
    """This event is emitted when an object is inserted into the DB."""


class ObjectUpdate(ObjectEvent):
    """This event is emitted when an object in the DB is updated."""


class ObjectDelete(ObjectEvent):
    """This event is emitted when an object is deleted from the DB."""

class UserDeleted(ObjectEvent):
    """This event is emitted when an user object is deleted from the DB."""


@subscriber(ObjectInsert)
def set_creation_date(event):
    """Set ``creation_date`` of the object that triggered the event.

    :param event: event that trigerred this handler.
    :type event: :class:`ObjectInsert`
    """

    obj = event.object
    if obj.creation_date is None:
        obj.creation_date = obj.modification_date = datetime.now()

@subscriber(ObjectInsert)
def set_meta(event):
    """Set ``meta_title``, ``meta_description`` and ``slug`` of the Content object.

    :param event: event that trigerred this handler.
    :type event: :class:`ObjectInsert`
    """
    obj = event.object
    if obj.meta_title is None:
        obj.meta_title = obj.title
    #TODO: handle meta_description generation from content if it has attr body
    if obj.slug is None:
        obj.slug = obj.generate_unique_slug()
    else:
        # If we have slug, make it unique
        obj.slug =title_to_slug(obj.slug, obj.slugs)

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