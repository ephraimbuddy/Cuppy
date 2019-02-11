import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound

from js.html5shiv import html5shiv
from cuppy.models import Document, ObjectInsert, ObjectUpdate
from cuppy.utils.util import title_to_slug
from cuppy.forms.content import AddDocument
from cuppy.fanstatic import edit_needed

log = logging.getLogger(__name__)

@view_config(route_name="dashboard", renderer="cuppy:templates/derived/dashboard/index.mako")
def dashboard(request):
    
    return dict()

@view_config(route_name="page", renderer="cuppy:templates/derived/dashboard/page.mako")
def page(request):
    """ This view lists all the pages/contents on the site"""
    edit_needed.need()
    docs = request.dbsession.query(Document).filter(Document.parent==None).all()
    return dict(docs = docs)


@view_config(route_name="add_doc", renderer="cuppy:templates/derived/document/add.mako")
def add_doc(request):
    edit_needed.need()
    parent_id = request.matchdict['parent_id']
    if parent_id:
        parent_id = parent_id[0]
        parent = Document.get_by_id(parent_id)
        if not parent:
            return HTTPNotFound()

    form=AddDocument(request.POST, meta={'csrf_context':request.session})
    
    if request.POST and form.validate():
        doc = Document(
            title = form.title.data,
            status = form.status.data,
            creation_date = form.creation_date.data,
            in_menu = form.in_menu.data,
            body = form.body.data,
            slug = form.slug.data,
            meta_title = form.meta_title.data,
            description = form.description.data,
        )
        request.dbsession.add(doc)
        event = ObjectInsert(doc, request, parent_id)
        request.registry.notify(event)
        return HTTPFound(location = request.route_url('page'))
    return dict(form=form, action_url= request.route_url('add_doc', parent_id=parent_id))



def add_document_callback(request, doc):

    return HTTPFound(location = request.route_url('view_doc', slug=doc.slug))

    
    
@view_config(route_name="edit_doc", renderer="cuppy:templates/derived/document/edit.mako")
def edit(request):
    edit_needed.need()
    slug = request.matchdict['slug']
    slug = slug[-1]
    doc = Document.get_by_slug(slug)
    if not doc:
        return HTTPNotFound()
    form = AddDocument(request.POST, meta={'csrf_context':request.session}, obj=doc)
    if request.POST and form.validate():
        form.populate_obj(doc)
        request.dbsession.merge(doc)
        event = ObjectUpdate(doc, request, parent_id=doc.parent_id)
        request.registry.notify(event)
        return HTTPFound(location = request.route_url('page'))
    return dict(form=form, action_url=request.route_url("edit_doc", slug=doc.get_slug()), doc=doc)
