from sqlalchemy import (Table, Column, Integer, Unicode,
 UnicodeText, func, ForeignKey, DateTime, Boolean)
from sqlalchemy.orm import relationship, selectinload

from .meta import Base, DBSession
from .nav import Nav


content_tags = Table("content_tags", Base.metadata,
Column('tag_id', ForeignKey('tags.id'), primary_key=True),
Column('content_id', ForeignKey('contents.id'), primary_key=True))


class Tag(Base):
    
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    contents = relationship("Content", back_populates='tags', secondary=content_tags)


class Content(Nav):

    __tablename__ = "contents"
    id= Column(Integer, ForeignKey('navs.id'), primary_key=True)
    title = Column(Unicode(255))
    # Description is used for summarizing the content. Appears after title in a document
    description = Column(UnicodeText)
    published = Column(Boolean(name="published"), default=True)
    creation_date = Column(DateTime)
    modification_date = Column(DateTime)
    in_navigation = Column(Boolean(name="in_navigation"))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="contents")
    tags = relationship('Tag', secondary=content_tags, back_populates='contents')

    __mapper_args__ = {
        'polymorphic_identity':'content'
    }

class Document(Content):
    " Document adds body and files to content"
    __tablename__ = 'documents'
    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    body = Column(UnicodeText)
    files = relationship("File", back_populates='document', cascade="all, delete, delete-orphan")
    
    __mapper_args__ = {
        'polymorphic_identity':'document'
    }



class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    posts = relationship('Post', back_populates="category")


class Post(Document):
    __tablename__ = "posts"
    id = Column(Integer, ForeignKey("documents.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="posts")
    

    @classmethod
    def get_query(cls, with_joinedload = True):
        query = DBSession.query(cls)
        if with_joinedload:
            query = query.options(selectinload(cls.tags))
        return query
    
    @classmethod
    def get_by_id(cls, id, with_joinedload=True):
        post = cls.get_query(with_joinedload)
        return post.filter(cls.id==id).first()
    
    @classmethod
    def post_bunch(cls, order_by, how_many=10, published=True, with_joinedload=True):
        posts = cls.get_query(with_joinedload)
        posts = posts.filter(published==published).order_by(order_by)
        return posts.limit(how_many).all()



class File(Base):
    " A file is an image,video etc addable to documents"
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    filename = Column(Unicode(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="files")
    document_id = Column(Integer, ForeignKey('documents.id'))
    document = relationship('Document', back_populates='files')
    
