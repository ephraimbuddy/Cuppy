import argparse
import sys
import logging

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from ..models.meta import Base
from ..models.nav import Nav
from ..models.content import Category, Document

log = logging.getLogger(__name__)


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """
    log.debug("Adding user ...")
    log.debug("Creating the index navigation")
    home = Document(name='', slug='', body="This is the home page")
    dbsession.add(home)
    dbsession.flush()
    log.debug('Creating Categories ...')
    category1 = Category(
        name="pyramid"
    )
    dbsession.add(category1)
    dbsession.flush()
    category2 = Category(name="Django")
    dbsession.add(category2)
    dbsession.flush()
    log.debug("creating documents ...")
    contact=Document(name = "Contact us",
                    body = "Contact us page",
                    slug='contact',
                    parent_id = home.id)
    dbsession.add(contact)
    dbsession.flush()
    projects = Document(name='projects',
                        slug = 'projects',
                        body="My projects",
                        parent_id=home.id)
    dbsession.add(projects)
    dbsession.flush()
    


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
