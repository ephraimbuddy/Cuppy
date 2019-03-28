import argparse
import sys
import logging

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from ..models.meta import Base
from ..models import User, Groups
log = logging.getLogger(__name__)


def setup_models(dbsession, request):
    """
    Add or update models / fixtures in the database.

    """
    if dbsession.query(User).count()<1:
        groups = ['superadmin', 'admin','owner','editor']
        for i in groups:
            g = Groups(i)
            dbsession.add(g)
        user = User(username=request.registry.settings['cuppy.admin_username'],
                email=request.registry.settings['cuppy.admin_email'],
                )
        dbsession.add(user)
        g = dbsession.query(Groups).filter_by(name='superadmin').first()
        user.mygroups.append(g)
        user.set_password(request.registry.settings['cuppy.admin_password'])
    

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
            request = env['request']
            dbsession = request.dbsession
            setup_models(dbsession, request)

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
