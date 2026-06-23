from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DataModel(Base):
    """Modelo de datos para análisis"""
    
    __tablename__ = "data_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Float)
    category = Column(String)
