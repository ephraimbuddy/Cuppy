from pyramid.view import view_config
from ...fanstatic import edit_needed
from js.html5shiv import html5shiv

@view_config(route_name="dashboard", renderer="cuppy:templates/derived/dashboard/index.mako")
def dashboard(request):
    
    return dict()