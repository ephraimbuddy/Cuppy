from sqlalchemy import Column, Unicode, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, backref

from .meta import DBSession, Base


class Nav(Base):
    __tablename__ = 'navs'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255),default="Untitled Node")
    path = Column(Unicode(255))
    parent_id = Column(Integer, ForeignKey(id))
    children = relationship("Nav",
                        cascade="all, delete,delete-orphan",
                        backref=backref("parent", remote_side=id)
                    )
    before = Column(Integer, default=None)
    type = Column(String(50), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity':'nav',
        'polymorphic_on':type
    }

class Section(Nav):
    __tablename__ = 'section'
    id = Column(Integer, ForeignKey('navs.id'), primary_key=True)
    
    __mapper_args__ = {'polymorphic_identity':'section'}