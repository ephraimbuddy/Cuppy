from pyramid.view import view_config



@view_config(route_name="dashboard", renderer="cuppy:templates/derived/dashboard/index.mako")
def dashboard(request):
    return dict()