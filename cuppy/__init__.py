from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_mako')
        config.include('.security')

        # routes
        config.include('.routes')
        config.include('.views.dashboard', route_prefix="dashboard")
        config.include('.views.document')
        
        config.scan()
    return config.make_wsgi_app()
