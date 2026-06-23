from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
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


class TarifaModel(Base):
    """Modelo de tarifas por producto"""
    
    __tablename__ = "tarifas"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(Integer, index=True)  # código para unir con productos.codigo_interno
    celda = Column(String)  # identifica la celda en Excel para almacenar el dato final
    t2025 = Column(Float)  # valor de tarifa en UF por tonelada para año 2025
    t2026 = Column(Float)  # valor de tarifa en UF por tonelada para año 2026


class CierreUFModel(Base):
    """Modelo de cierres de UF por ciclo"""
    
    __tablename__ = "cierres_uf"
    
    id = Column(Integer, primary_key=True, index=True)
    ciclo = Column(String, index=True, unique=True)  # ciclo en formato YYYYMM (ej: "202501")
    uf_pesos = Column(Float)  # valor de UF en pesos al cierre del mes


class DataProcesadaModel(Base):
    """Modelo de datos procesados con resultados de la lógica de cálculo"""
    
    __tablename__ = "data_procesada"
    __table_args__ = (
        UniqueConstraint('codigo_interno', 'periodo', name='uq_codigo_periodo'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_interno = Column(Integer, index=True)  # código usado en tarifas.json y productos.codigo_interno
    celda = Column(String)  # celda obtenida de tarifas.celda
    categoria = Column(String, index=True)  # de productos.categoria
    subcategoria = Column(String, index=True)  # de productos.subcategoria
    tipo_material = Column(String)  # de productos.tipo_material
    material = Column(String)  # de productos.material
    riesgo = Column(String)  # de productos.riesgo
    total_tonelada = Column(Float)  # suma de cantidad * peso_ton por codigo_interno
    total_gramos = Column(Float)  # suma de cantidad * peso_gr por codigo_interno
    cantidad_total = Column(Float)  # cantidad total de productos vendidos por codigo_interno
    total_uf = Column(Float)  # suma total en UF de todos los productos vendidos
    total_clp = Column(Float)  # total_uf * valor de cierreUF según periodo
    periodo = Column(String, index=True)  # periodo en formato YYYYMM
