from pyramid.config import Configurator
from cuppy.utils.util import get_module

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    config = default_config(global_config, **settings)
    # routes
    config.include('.routes')
    config.include('.views.dashboard', route_prefix="dashboard")
    config.include('.views.document')
    
    config.scan()
    return config.make_wsgi_app()


default_settings = {
        'cuppy.url_normalizer':'cuppy.utils.util.url_normalizer',
        'cuppy.timezone':'Africa/Lagos',
        'cuppy.csrf_secret':b'bjuiewbju43/s',
        'cuppy.csrf_class':'cuppy.forms.csrf_class',
        'cuppy.csrf':True,
        'cuppy.csrf_time_limit':20,
        'cuppy.email_secret':"jkasdfg8349c4ewu7438fiu73",
        'cuppy.email_secret_password':'skdsidud782387dsdhjdsd7dsds',
        'cuppy.confirm_token_expiration':86400,
        'cuppy.minified_css':True,
        'cuppy.minified_js':True,
        'cuppy.static_path':'cuppy/static',
        'cuppy.site_url':'https://www.nairabricks.com',
    }

conf_dotted = {
    'cuppy.url_normalizer',
    'cuppy.csrf_class'
}

def _resolve_dotted(d,keys=conf_dotted):
    resolved = d.copy()
    for key in conf_dotted:
        value = resolved[key]
        if not isinstance(value, str):
            continue
        new_value = []
        for name in value.split():
            new_value.append(get_module(name))
        resolved[key] = new_value
    return resolved

def default_config(global_config, **settings):
    
    for key, value in default_settings.items():
        settings.setdefault(key, value)
    for key, value in settings.items():
        if key.startswith("cuppy") and isinstance(value, bytes):
            settings[key] = value.decode("utf8")
    
    settings = _resolve_dotted(settings)
    with Configurator(settings=settings) as config:
        #Include cuppy modules
        for module in settings["cuppy.includes"]:
            config.include(module)
        pyramid_includes = config.registry.settings['pyramid.includes']
        # Modules in 'pyramid.includes'  may
        # override 'cuppy.includes':
        if pyramid_includes:
            for module in pyramid_includes.split():
                config.include(module)
        config.include('pyramid_mako')
        config.include('.models')
        config.include('.security')

    return config
