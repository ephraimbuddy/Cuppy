from pyramid.view import view_config

from ..models.blog import Post


@view_config(route_name="home", renderer="codepython:templates/index.mako")
def home(request):
    posts = request.dbsession.query(Post).all()
    return dict(posts=posts)
