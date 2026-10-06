from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    topic = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=False)
    module_type = Column(String(50), nullable=False)
    content = Column(Text)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class CachedSearch(Base):
    __tablename__ = "cached_searches"
    id = Column(Integer, primary_key=True)
    query = Column(String(500), nullable=False, unique=True)
    results_json = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
