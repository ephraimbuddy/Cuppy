from base64 import b64encode
from sqlalchemy import engine_from_config
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from cuppy.utils.util import get_module
from cuppy.models import DBSession, Base




def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    session_factory = session_factory_from_settings(settings)

    with default_config(global_config, **settings) as config:
        config.set_session_factory(session_factory)
    
        # use pyramid_tm to hook the transaction lifecycle to the request
        config.include('pyramid_tm')
        config.add_request_method(lambda r: DBSession,'dbsession',reify=True)
        # use pyramid_retry to retry a request when transient exceptions occur
        config.include('pyramid_retry')
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
        'cuppy.includes': ' '.join(
                            ['cuppy.security',
                            'cuppy.routes',
                            'cuppy.views.edit',
                            'cuppy.views.view']
        ),
        
        'cuppy.templates.api':'cuppy.views.util.TemplateApi',
        'cuppy.site_title':'Cuppy'
    }

conf_dotted = {
    'cuppy.url_normalizer',
    'cuppy.includes',
    'cuppy.templates.api'
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
            config.include(module)
        pyramid_includes = config.registry.settings['pyramid.includes']

        
        # Modules in 'pyramid.includes'  may
        # override 'cuppy.includes':
        if pyramid_includes:
            for module in pyramid_includes.split():
                config.include(module)
        config.include('pyramid_mako')
        config.include('pyramid_deform')
    
    return config
