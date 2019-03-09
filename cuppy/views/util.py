from pyramid.decorator import reify
from pyramid.renderers import render

from cuppy.utils.util import get_settings
from cuppy.models import Document

def template_api(context, request, **kwargs):
    return get_settings()["cuppy.templates.api"][0](context, request, **kwargs)


def add_global_renderer(event):
    if event.get("renderer_name") != "json":
        request = event["request"]
        api = getattr(request, "template_api", None)
        if api is None and request is not None:
            api = template_api(event["context"], event["request"])
        event["api"] = api

class TemplateApi(object):
    
    def __init__(self, context, request, **kwargs):
        self.context = context
        self.request = request

        if getattr(request, "template_api", None) is None:
            request.template_api = self
        
        self.settings = get_settings()
        self.__dict__.update(kwargs)

    
    def __lineage__(self):
        try:
            context = self.context.obj
        except AttributeError:
            context = None
        while context is not None:
            yield context
            try:
                context = context.parent
            except AttributeError:
                context = None
    @reify          
    def lineage(self):
        return list(self.__lineage__())

    @reify
    def root(self):
        return self.lineage[-1]

    @reify 
    def breadcrumbs(self):

        breadcrumbs = self.lineage
        # If the breadcrumbs is empty then the object is not a doc_factory object
        if len(list(breadcrumbs))<1:
            return False
        return reversed(breadcrumbs)

    @reify
    def site_title(self):
        value = get_settings().get("cuppy.site_title")
        if not value:
            value = self.root.title
        return value

    @reify
    def page_title(self):
        try:
            title = self.context.obj.title
        except AttributeError:
            return self.site_title
        return title
    
    @reify
    def meta_keywords(self):
        try:
            tags = self.context.obj.tags
        except AttributeError:
            return ''
        pass
    
    @reify
    def meta_description(self):
        try:
            description =self.context.obj.description
        except AttributeError:
            return ''
        return description or ''
            
    
    def current_page(self, o):
        # Check if factory is doc_factory or RootFactory. 
        # The context for a root factory does not have obj attribute
        try:
            obj = self.context.obj
        except AttributeError:
            return False
        if o.id==self.context.obj.id:
            return True
        return False

    def render_template(self, template, **kwargs):

        return render(template, kwargs, self.request)

    
    @reify
    def navigation_documents(self):
        contents = self.request.dbsession.query(Document).filter(Document.parent==None).\
        filter(Document.in_menu==True).all()
        return contents

    @reify
    def home(self):
        if self.request.url==self.request.route_url('home'):
            return True
        return False
    