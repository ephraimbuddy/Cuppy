import unittest
from pyramid.paster import bootstrap
from pyramid.request import Request
from pyramid import testing
import transaction


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('codepython.models')
        settings = self.config.get_settings()
        
        from codepython.models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)
        

    def init_database(self):
        from codepython.models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from codepython.models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)
    
    def makeUser(self, username, email,first_name=None, last_name=None):
        from codepython.models.users import User
        user = User(first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email)
        return user
