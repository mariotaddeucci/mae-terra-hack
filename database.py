from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from os import getenv

Model = declarative_base()


class Produto(Model):
    __tablename__ = 'produto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    clarifai_id = Column(String(255))
    message = Column(String(255))
    tags = relationship("Tag", backref="produto")


class Tag(Model):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(255))
    produto_id = Column(Integer, ForeignKey(Produto.__tablename__ + '.id'), nullable=False)


engine = create_engine(getenv('SQLALCHEMY_URI'))
Model.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))