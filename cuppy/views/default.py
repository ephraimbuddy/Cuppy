from pyramid.view import view_config

from ..fanstatic import view_needed
from ..models.content import Document


@view_config(route_name="home", renderer="cuppy:templates/index.mako")
def home(request):
    view_needed.need()
    home_page_name='' #Just a string
    doc = Document.get_by_name(home_page_name)
    return dict(doc = doc)
