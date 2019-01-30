from itsdangerous import URLSafeTimedSerializer
import re
from unidecode import unidecode
import os.path
import os

from pyramid.settings import asbool
from pyramid.util import DottedNameResolver
from pyramid.threadlocal import get_current_registry
from pyramid.security import remember


# Define and compile static regexes
# The below codes are partly from Kotti CMS


FILENAME_REGEX = re.compile(r"^(.+)\.(\w{,4})$", re.U)
IGNORE_REGEX = re.compile(r"['\"]", re.U)
URL_DANGEROUS_CHARS_REGEX = re.compile(r"[!#$%&()*+,/:;<=>?@\\^{|}\[\]~`]+", re.U)
MULTIPLE_DASHES_REGEX = re.compile(r"\-+", re.U)
EXTRA_DASHES_REGEX = re.compile(r"(^\-+)|(\-+$)", re.U)
# Define static constraints
MAX_LENGTH = 200
MAX_URL_LENGTH = 50


def crop_name(base, maxLength=MAX_LENGTH):
    baseLength = len(base)

    index = baseLength
    while index > maxLength:
        index = base.rfind('-', 0, index)

    if index == -1 and baseLength > maxLength:
        base = base[:maxLength]

    elif index > 0:
        base = base[:index]

    return base


def url_normalizer(text, locale=None, max_length=MAX_URL_LENGTH):

    text = unidecode(text)

    # lowercase text
    base = text.lower()
    ext = ''

    m = FILENAME_REGEX.match(base)
    if m is not None:
        base = m.groups()[0]
        ext = m.groups()[1]

    base = base.replace(' ', '-')
    base = IGNORE_REGEX.sub('', base)
    base = URL_DANGEROUS_CHARS_REGEX.sub('-', base)
    base = EXTRA_DASHES_REGEX.sub('', base)
    base = MULTIPLE_DASHES_REGEX.sub('-', base)


    base = crop_name(base, maxLength=max_length)

    if ext != '':
        base = base + '.' + ext
    return base

def disambiguate_name(name):
    parts = name.split('-')
    if len(parts) > 1:
        try:
            index = int(parts[-1])
        except ValueError:
            parts.append('1')
        else:
            parts[-1] = ""+(index + 1)

    else:
        parts.append('1')
    return '-'.join(parts)


def title_to_slug(title, blacklist=(), max_length=200):
    blacklist = [i.lower() for i in blacklist]
    normalizer = cuppy_settings('url_normalizer')[0]
    name = normalizer(title, locale='en', max_length=max_length)
    if name not in blacklist:
        return name
    while name in blacklist:
        name = disambiguate_name(name)
    return name


def get_settings():
    return get_current_registry().settings

def cuppy_settings(key):
    """ Gets a cuppy setting if the key is set 
    """
    settings = get_settings()

    return settings.get('cuppy.%s' % key)
    

def get_module(package):
    """ Returns a module based on the string passed
    """
    resolver = DottedNameResolver(package.split('.', 1)[0])
    return resolver.resolve(package)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(cuppy_settings('email_secret'))
    return serializer.dumps(email, salt=cuppy_settings('email_secret_password'))


def confirm_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(cuppy_settings('email_secret'))
    ex= cuppy_settings("confirm_token_expiration")
    if ex:
        expiration = ex
    try:
        email = serializer.loads(
            token,
            salt=cuppy_settings('email_secret_password'),
            max_age=expiration
        )
    except:
        return False
    return email


core_css = ['bootstrap','fontawesome', 'adminlte']


class StaticResource(object):
    """ A class to enable addition of static resources to project"""
    def __init__(self, resources:list=None, css:bool=True):
        
        self.is_css = css

        if not resources:
            resources =[]
        if not isinstance(resources, list):
            raise ValueError("resources must be a list of strings or a list of StaticResource object")
        self.resources = []
        self.css_resources =[]
        self.js_resources = []
        for resource in resources:
            self.add(resource)

    def add(self, resource):
        if isinstance(resource,self.__class__):
            self.resources.extend(resource.resources)
        elif isinstance(resource,str):
            if self.is_css:
                #deal with css files
                if asbool(cuppy_settings('minified_css')):
                    self.css_resources.append('.'.join([resource,'min','css']))
                    self.resources.append('.'.join([resource,'min','css']))
                else:
                    self.css_resources.append('.'.join([resource,'min','css']))
                    self.resources.append('.'.join([resource,'css']))
            else:
                if asbool(cuppy_settings('minified_js')):
                    self.js_resources.append('.'.join([resource,'min','js']))
                    self.resources.append('.'.join([resource,'min','js']))
                else:
                    self.js_resources.append('.'.join([resource,'min','js']))
                    self.resources.append('.'.join([resource,'js']))
        else:
            raise ValueError("resource must be of type string or  StaticResource Object")

    def list_js_resources(self):
        site_url = cuppy_settings('site_url')
        search_path = cuppy_settings('static_path')
        js = []
        for root, dirnames, files in os.walk(search_path):
            for file in self.js_resources:
                if file in files:
                    js.append(os.path.join(site_url,root,file))
        return js



    