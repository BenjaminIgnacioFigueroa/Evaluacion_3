from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductoModel(Base):
    """Modelo de productos de reciclaje"""
    
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_erp = Column(String, index=True, unique=True)
    nombre = Column(String, index=True)
    peso_ton = Column(Float)
    peso_gr = Column(Float)
    codigo_interno = Column(Integer)
    categoria = Column(String, index=True)
    subcategoria = Column(String, index=True)
    tipo_material = Column(String)
    material = Column(String)
    riesgo = Column(String)
