import bcrypt

from .meta import Base, DBSession
from sqlalchemy import Unicode, UnicodeText, Column, Integer, DateTime,Enum, ForeignKey, Table, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS, Everyone


user_group = Table('user_group', Base.metadata,
    Column('user_id', Integer, ForeignKey("users.id", onupdate='CASCADE', ondelete='CASCADE')),
    Column('group_id',Integer, ForeignKey("auth_groups.id", onupdate='CASCADE', ondelete='CASCADE')))


# need to create Unique index on (user_id,group_id)
Index('user_group_index', user_group.c.user_id, user_group.c.group_id)


class Groups(Base):
    """ Table name: auth_groups
    """
    __tablename__ = 'auth_groups'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(80), unique=True, nullable=False)
    description = Column(Unicode(255), default=u'')

    users = relationship('User', secondary=user_group,
                     back_populates='mygroups')

    def __repr__(self):
        return u'%s' % self.name

    @classmethod
    def get_all(cls):
        return DBSession.query(cls).all()
    
    @classmethod
    def get_by_id(cls,id_):
        return DBSession.query(cls).get(id_)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(50), nullable=False, unique=True)
    email = Column(Unicode(50), nullable=False)
    password_hash = Column(UnicodeText)
    first_name = Column(Unicode(50))
    last_name = Column(Unicode(50))
    about = Column(UnicodeText)
    #joined_date = Column(DateTime, default = func.now())
    mygroups = relationship("Groups", secondary=user_group, back_populates="users")
    contents = relationship('Content', back_populates="user")
    user_log = relationship('AuthUserLog', back_populates='user', cascade='all, delete, delete-orphan')
    activities = relationship('SiteActivity', back_populates='user')
  
    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False

    @property
    def fullname(self):
        if self.first_name:
            return self.first_name+' '+self.last_name
        return self.username
    
    @classmethod
    def get_by_id(cls,id):
        obj= DBSession.query(cls).get(id)
        return obj

    @classmethod
    def get_by_username(cls, username):
        obj = DBSession.query(cls).filter_by(username=username).first()
        return obj
    
    @property
    def last_login(self):
        q =[x for x in self.user_log if x.event=="L"]
        if len(q)>0:
            return q[-1].time
        q = [x for x in self.user_log if x.event=='R']
        if len(q)>0:
            return q[-1].time
        return 'never'

    @classmethod
    def get_by_email(cls, email):
        obj = DBSession.query(cls).filter_by(email=email).first()
        return obj

    
class AuthUserLog(Base):
    """
    event:
      L - Login
      R - Register
      P - Password
      F - Forgot
    """
    __tablename__ = 'auth_user_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship(User, back_populates='user_log')
    time = Column(DateTime(), default=func.now())
    ip_addr = Column(Unicode(39), nullable=False)
    event = Column(Enum(u'L',u'R',u'P',u'F', name=u'event'), default=u'L')


class SiteActivity(Base):
    """ Records every activity on the site by user
    :
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User",back_populates="activities")
    description = Column(Unicode(100))
    time = Column(DateTime, default=func.now())
    """
    __tablename__ = 'site_activity'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User",back_populates="activities")
    description = Column(Unicode(100))
    time = Column(DateTime, default=func.now())




    


