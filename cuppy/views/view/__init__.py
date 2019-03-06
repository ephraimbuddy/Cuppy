from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import ALL_PERMISSIONS
from pyramid.httpexceptions import HTTPNotFound

from ...models.content import Document
from ...security import SITE_ACL

def includeme(config):
    config.add_route("view_doc", 'page/*slug', factory=doc_factory)
    


def doc_factory(request):
    slug = request.matchdict['slug']
    slug = slug[-1]
    doc = Document.get_by_slug(slug)
    if doc is None:
        raise HTTPNotFound()
    return DocumentResource(doc)
    

class DocumentResource(object):
    def __init__(self,object):
       self.obj = object
        
    def __acl__(self):
        acl = SITE_ACL
        acl.append((Allow, str(self.obj.user.id),('edit','state_change')))
        return acl
    
  
        

    