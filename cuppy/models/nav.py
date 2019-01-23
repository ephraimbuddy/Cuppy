from sqlalchemy import Column, Unicode, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from ..utils.util import title_to_name
from .meta import DBSession, Base


class Nav(Base):
    __tablename__ = 'navs'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(250), nullable=False)
    title = Column(Unicode(250))
    slug = Column(String(2000), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey(id))
    children = relationship("Nav",
                        cascade="all, delete,delete-orphan",
                        backref=backref("parent", remote_side=id)
                    )
    type = Column(String(50), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity':'nav',
        'polymorphic_on':type
    }

    def keys(self):
        return [child.name for child in self.children]

    def values(self):
        return self.children

    def get_slug(self):
        
        return self.slug

    def generate_unique_slug(self):
        query = [i.name for i in DBSession.query(Nav).all()]
        return title_to_name(self.get_slug,query)