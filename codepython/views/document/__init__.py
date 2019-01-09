from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import ALL_PERMISSIONS
from pyramid.httpexceptions import HTTPNotFound

from ...models.content import Document


def includeme(config):
    
    config.add_route('add_doc', 'create')
    config.add_route("view_doc", '{id}/view', factory=factory, traverse='/{id}')
    config.add_route("edit_doc", '{id}/update')
    config.add_route("delete_doc", '{id}/delete')


def factory(request):
    id = request.matchdict['id']
    doc = Document.get_by_id(id)
    if doc is None:
        raise HTTPNotFound()
    return DocumentResource(doc)
    

class DocumentResource(object):
    def __init__(self,document):
       self.document = document

    def __acl__(self):

        return [(Allow, Authenticated, 'post'),
                (Allow,'superadmin',ALL_PERMISSIONS),
                (Allow, 'admin',('admin','supermod','mod','edit')),
                (Allow, 'supermod',('supermod','mod')),
                (Allow, 'mod','mod')]

    