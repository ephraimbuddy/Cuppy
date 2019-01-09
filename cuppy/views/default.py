from pyramid.view import view_config

from ..models.content import Post


@view_config(route_name="home", renderer="cuppy:templates/index.mako")
def home(request):
    posts = request.dbsession.query(Post).all()
    return dict(posts=posts)
