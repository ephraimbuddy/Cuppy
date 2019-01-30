from base64 import b64encode

from pyramid.config import Configurator

from cuppy.utils.util import get_module





def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    with default_config(global_config, **settings) as config:
        config.scan()
    return config.make_wsgi_app()


default_settings = {
        'cuppy.url_normalizer':'cuppy.utils.util.url_normalizer',
        'cuppy.timezone':'Africa/Lagos',
        'cuppy.csrf_secret_key':b'\xb6\xb9\xdf\xb3\x85u$i<{\xe3^\xc3\xf3N\xab',
        'cuppy.csrf_time_limit':20,
        'cuppy.email_secret':"jkasdfg8349c4ewu7438fiu73",
        'cuppy.email_secret_password':'skdsidud782387dsdhjdsd7dsds',
        'cuppy.confirm_token_expiration':86400,
        'cuppy.minified_css':True,
        'cuppy.minified_js':True,
        'cuppy.site_url':'',
        'cuppy.includes': ' '.join(
                            ['cuppy.models',
                            'cuppy.security',
                            'cuppy.routes',
                            'cuppy.views.edit',
                            'cuppy.views.document']
        ),
        'cuppy.session_factory':'cuppy.security.session_factory'
    }

conf_dotted = {
    'cuppy.url_normalizer',
    'cuppy.includes',
    'cuppy.session_factory'
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
        if key == "cuppy.csrf_secret_key":
            settings[key] = str.encode(value)
    
    settings = _resolve_dotted(settings)
    with Configurator(settings=settings) as config:
        #Include cuppy modules
        for module in settings["cuppy.includes"]:
            if module==get_module('cuppy.views.edit'):
                config.include(module, route_prefix='dashboard')
            print(module)
            config.include(module)
        pyramid_includes = config.registry.settings['pyramid.includes']

        
        # Modules in 'pyramid.includes'  may
        # override 'cuppy.includes':
        if pyramid_includes:
            for module in pyramid_includes.split():
                config.include(module)
        config.include('pyramid_mako')
        
    
    return config
