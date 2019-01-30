from pyramid.view import view_config

from cuppy.fanstatic import view_needed

class DocumentView(object):

    def __init__(self,request):
        self.request = request
        self.session = request.session
        self.context = request.context

    @view_config(route_name="view_doc",renderer="cuppy:templates/derived/document/view.mako")
    def doc_view(self):
        view_needed.need()
        context = self.context.document
        return dict(document=context)

    