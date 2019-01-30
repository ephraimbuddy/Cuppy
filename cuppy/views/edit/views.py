from pyramid.view import view_config

from js.html5shiv import html5shiv
from cuppy.models.content import Document
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
        doc = Document(form.data)
        # Handle meta TODO: use events for meta and user addition
        doc.meta_title = doc.get_meta_title()
        doc.description = doc.get_description()
        if not form.data.slug:
            doc.slug = doc.generate_unique_slug()
        else:
            doc.slug = title_to_slug(form.data.slug, doc.slugs)
        doc.user = request.user
        request.dbsession.add(doc)
            
        return add_document_callback(request,doc)
    return dict(form=form)


def add_document_callback(request, doc):

    return request.route_url('view_doc', name=doc.name)

    
    
@view_config(route_name="edit_doc", renderer="cuppy:templates/derived/document/edit.mako")
def edit(request):
    pass