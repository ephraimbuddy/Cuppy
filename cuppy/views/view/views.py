from pyramid.view import view_config


class DocumentView(object):

    def __init__(self,request):
        self.request = request
        self.session = request.session
        self.context = request.context

    @view_config(route_name="view_doc", renderer="cuppy:templates/derived/document/document.mako")
    def doc_view(self):
        
        context = self.context.obj
        return dict(document=context)

    

    

    