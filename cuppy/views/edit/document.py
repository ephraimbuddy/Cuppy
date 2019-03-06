import logging
from datetime import datetime
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound

from cuppy.models import Document, ObjectInsert, ObjectUpdate, ObjectDelete, Tag, DBSession
from cuppy.utils.util import title_to_slug
from cuppy.forms.content import AddDocument


log = logging.getLogger(__name__)


@view_config(route_name="dashboard", renderer="cuppy:templates/derived/dashboard/index.mako")
def dashboard(request):
    
    return dict()

@view_config(route_name="page", renderer="cuppy:templates/derived/dashboard/page.mako")
def page(request):
    """ This view lists all the pages/contents on the site"""
    
    docs = request.dbsession.query(Document).filter(Document.parent==None).all()
    return dict(docs = docs)


@view_config(route_name="add_doc", renderer="cuppy:templates/derived/document/add.mako")
def add_doc(request):
    
    parent_id = request.matchdict['parent_id']
    if parent_id:
        parent_id = parent_id[0]
        parent = Document.get_by_id(parent_id)
        if not parent:
            return HTTPNotFound()
    # If we have parent_id value, we are now sure that it's valid
    form=AddDocument(request.POST, meta={'csrf_context':request.session})
    if request.POST and form.validate():
        appstruct = form.data
        appstruct.pop('csrf_token')
        doc= Document(**appstruct)
        request.dbsession.add(doc)
        event = ObjectInsert(doc, request, parent_id)
        request.registry.notify(event)
        return HTTPFound(location = request.route_url('page'))
    return dict(form=form, action_url= request.route_url('add_doc', parent_id=parent_id))



def add_document_callback(request, doc):

    return HTTPFound(location = request.route_url('view_doc', slug=doc.slug))

    
    
@view_config(route_name="edit_doc", renderer="cuppy:templates/derived/document/edit.mako")
def edit(request):
    
    slug = request.matchdict['slug']
    slug = slug[-1]
    doc = request.dbsession.query(Document).filter(Document.slug==slug).first()
    if not doc:
        return HTTPNotFound()
    form = AddDocument(request.POST, meta={'csrf_context':request.session}, obj=doc)
    
    if request.POST and form.validate():
        appstruct = form.data
        appstruct.pop("csrf_token")
        appstruct['slug'] = doc.change_slug(appstruct['slug'])
        for k, v in appstruct.items():
            setattr(doc, k, v)
        request.dbsession.merge(doc)
        event = ObjectUpdate(doc, request, parent_id=doc.parent_id)
        request.registry.notify(event)
        return HTTPFound(location = request.route_url('page'))
    return dict(form=form, action_url=request.route_url("edit_doc", slug=doc.get_slug()), doc=doc)

@view_config(route_name="delete_doc")
def delete_doc(request):
    doc = request.context.obj
    if not doc:
        return HTTPNotFound()
    request.dbsession.delete(doc)
    event = ObjectDelete(doc, request,doc.parent_id)
    request.registry.notify(event)
    return HTTPFound(location = request.route_url('page'))
