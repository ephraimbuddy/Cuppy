from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import ALL_PERMISSIONS
from pyramid.httpexceptions import HTTPNotFound

from ...models.content import Document
from ...security import SITE_ACL

def includeme(config):
    
    config.add_route('add_doc', 'create')
    config.add_route("view_doc", '{slug}', factory=factory)
    config.add_route("edit_doc", '{slug}/update')
    config.add_route("delete_doc", '{slug}/delete')


def factory(request):
    slug = request.matchdict['slug']
    parts = slug.split('/')
    if len(parts)>1:
        name = parts[-1]
    name=slug
    doc = Document.get_by_name(name)
    
    if doc is None:
        raise HTTPNotFound()
    return DocumentResource(doc)
    

class DocumentResource(object):
    def __init__(self,document):
       self.document = document

    def __acl__(self):
        acl = SITE_ACL
        acl.append((Allow, str(self.document.user.id),('edit','state_change')))
        return acl
    
  
        

    