from pyramid.view import view_config
from cuppy.models.content import Document


@view_config(route_name="view_doc",renderer="cuppy:templates/derived/document/view.mako")
def doc_view(request):
    document = request.context.document
    #document = Document.get_by_id(id)

    return dict(document=document)

class DocumentView(object):

    def __init__(self,request):
        self.request = request
        self.session = request.session

    @view_config(route_name="add_doc", renderer="cuppy:templates/derived/document/add.mako")
    def add(self):
        pass
    
    @view_config(route_name="edit_doc", renderer="cuppy:templates/derived/document/edit.mako")
    def edit(self):
        pass