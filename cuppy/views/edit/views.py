from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from js.html5shiv import html5shiv
from cuppy.models import Document, ObjectInsert
from cuppy.utils.util import title_to_slug
from cuppy.forms.content import AddDocument
from cuppy.fanstatic import edit_needed


@view_config(route_name="dashboard", renderer="cuppy:templates/derived/dashboard/index.mako")
def dashboard(request):
    
    return dict()


@view_config(route_name="add_doc", renderer="cuppy:templates/derived/document/add.mako")
def add_doc(request):
    edit_needed.need()
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
            description = form.description.data
        )
        request.dbsession.add(doc)
        event = ObjectInsert(doc, request)
        request.registry.notify(event)
        #TODO: handle meta description generation in event
        
        return HTTPFound(location = request.route_url('view_doc', slug=doc.slug))
    return dict(form=form)


def add_document_callback(request, doc):

    return HTTPFound(location = request.route_url('view_doc', slug=doc.slug))

    
    
@view_config(route_name="edit_doc", renderer="cuppy:templates/derived/document/edit.mako")
def edit(request):
    pass