from pyramid.view import view_config
from cuppy.models.content import Document


class DocumentView(object):

    def __init__(self,request):
        self.request = request
        self.session = request.session
        self.context = request.context

    @view_config(route_name="view_doc",renderer="cuppy:templates/derived/document/view.mako")
    def doc_view(self):
        document = self.context.document
        return dict(document=document)

    @view_config(route_name="add_doc", renderer="cuppy:templates/derived/document/add.mako")
    def add(self):
        pass
    
    @view_config(route_name="edit_doc", renderer="cuppy:templates/derived/document/edit.mako")
    def edit(self):
        pass