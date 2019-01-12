from pyramid.view import view_config

from ..models.content import Document


@view_config(route_name="home", renderer="cuppy:templates/index.mako")
def home(request):
    home_page_name=''
    doc = Document.get_by_name(home_page_name)
    return dict(doc = doc)
