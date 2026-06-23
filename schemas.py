from pydantic import BaseModel
from typing import Optional


class DataBase(BaseModel):
    """Schema base para datos"""
    name: str
    value: float
    category: str


class DataCreate(DataBase):
    """Schema para crear datos"""
    pass


class DataResponse(DataBase):
    """Schema para respuesta de datos"""
    id: int
    
    class Config:
        from_attributes = True


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
