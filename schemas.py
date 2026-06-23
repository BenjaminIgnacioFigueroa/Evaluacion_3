from pydantic import BaseModel
from typing import Optional


class ProductoBase(BaseModel):
    """Schema base para productos"""
    codigo_erp: str
    nombre: str
    peso_ton: float
    peso_gr: float
    codigo_interno: int
    categoria: str
    subcategoria: str
    tipo_material: str
    material: str
    riesgo: str


class ProductoCreate(ProductoBase):
    """Schema para crear productos"""
    pass


class ProductoResponse(ProductoBase):
    """Schema para respuesta de productos"""
    id: int
    
    class Config:
        from_attributes = True


class ProductoUpdate(BaseModel):
    """Schema para actualizar productos (todos los campos opcionales)"""
    codigo_erp: Optional[str] = None
    nombre: Optional[str] = None
    peso_ton: Optional[float] = None
    peso_gr: Optional[float] = None
    codigo_interno: Optional[int] = None
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None
    tipo_material: Optional[str] = None
    material: Optional[str] = None
    riesgo: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Schema para respuesta de análisis"""
    media: float
    desviacion: float
    maximo: float
    minimo: float
    datos: list[float]


class HealthResponse(BaseModel):
    """Schema para health check"""
    status: str
    database_connected: bool
    database_url_configured: bool
