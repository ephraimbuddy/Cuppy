import re

# Define and compile static regexes

from unidecode import unidecode

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


def title_to_name(title, query_set=(), max_length=200):
    query_set = [i.lower() for i in query_set]
    name = url_normalizer(title, locale='en', max_length=max_length)
    while name in query_set:
        name = disambiguate_name(name)
    return name