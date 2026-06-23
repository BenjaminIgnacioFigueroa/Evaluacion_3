from sqlalchemy import Column, Integer, String, Float, ForeignKey
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


class VentaUnitariaModel(Base):
    """Modelo de ventas unitarias mensuales"""
    
    __tablename__ = "ventas_unitarias"
    
    id = Column(Integer, primary_key=True, index=True)
    ciclo = Column(String, index=True)  # mes y año de la venta (ej: "2025-01")
    codigo_erp = Column(String, index=True)  # código del producto vendido
    cantidad = Column(Float)  # total vendido en el mes/año correspondiente
