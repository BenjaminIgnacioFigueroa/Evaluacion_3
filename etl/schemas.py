from pydantic import BaseModel, field_serializer
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


class VentaUnitariaBase(BaseModel):
    """Schema base para ventas unitarias"""
    ciclo: str
    codigo_erp: str
    cantidad: float


class VentaUnitariaCreate(VentaUnitariaBase):
    """Schema para crear ventas unitarias"""
    pass


class VentaUnitariaResponse(VentaUnitariaBase):
    """Schema para respuesta de ventas unitarias"""
    id: int
    
    class Config:
        from_attributes = True


class VentaUnitariaUpdate(BaseModel):
    """Schema para actualizar ventas unitarias (todos los campos opcionales)"""
    ciclo: Optional[str] = None
    codigo_erp: Optional[str] = None
    cantidad: Optional[float] = None


class VentaConProductoResponse(BaseModel):
    """Schema para respuesta de ventas unitarias con información del producto"""
    id: int
    ciclo: str
    codigo_erp: str
    cantidad: float
    producto_nombre: Optional[str] = None
    producto_peso_ton: Optional[float] = None
    producto_peso_gr: Optional[float] = None
    producto_codigo_interno: Optional[int] = None
    producto_categoria: Optional[str] = None
    producto_subcategoria: Optional[str] = None
    producto_tipo_material: Optional[str] = None
    producto_material: Optional[str] = None
    producto_riesgo: Optional[str] = None


class TarifaBase(BaseModel):
    """Schema base para tarifas"""
    codigo: int
    celda: str
    t2025: float
    t2026: float


class TarifaCreate(TarifaBase):
    """Schema para crear tarifas"""
    pass


class TarifaResponse(TarifaBase):
    """Schema para respuesta de tarifas"""
    id: int
    
    class Config:
        from_attributes = True


class TarifaUpdate(BaseModel):
    """Schema para actualizar tarifas (todos los campos opcionales)"""
    codigo: Optional[int] = None
    celda: Optional[str] = None
    t2025: Optional[float] = None
    t2026: Optional[float] = None


class VentaCompletaResponse(BaseModel):
    """Schema para respuesta de ventas unitarias con producto y tarifa"""
    id: int
    ciclo: str
    codigo_erp: str
    cantidad: float
    producto_nombre: Optional[str] = None
    producto_peso_ton: Optional[float] = None
    producto_peso_gr: Optional[float] = None
    producto_codigo_interno: Optional[int] = None
    producto_categoria: Optional[str] = None
    producto_subcategoria: Optional[str] = None
    producto_tipo_material: Optional[str] = None
    producto_material: Optional[str] = None
    producto_riesgo: Optional[str] = None
    tarifa_celda: Optional[str] = None
    tarifa_t2025: Optional[float] = None
    tarifa_t2026: Optional[float] = None


class CierreUFBase(BaseModel):
    """Schema base para cierres de UF"""
    ciclo: str
    uf_pesos: float


class CierreUFCreate(CierreUFBase):
    """Schema para crear cierres de UF"""
    pass


class CierreUFResponse(CierreUFBase):
    """Schema para respuesta de cierres de UF"""
    id: int
    
    class Config:
        from_attributes = True


class CierreUFUpdate(BaseModel):
    """Schema para actualizar cierres de UF (todos los campos opcionales)"""
    ciclo: Optional[str] = None
    uf_pesos: Optional[float] = None


class DataProcesadaBase(BaseModel):
    """Schema base para datos procesados"""
    codigo_interno: int
    celda: str
    categoria: str
    subcategoria: str
    tipo_material: str
    material: str
    riesgo: str
    total_tonelada: float
    total_gramos: float
    cantidad_total: float
    total_uf: float
    total_clp: float
    periodo: str


class DataProcesadaCreate(DataProcesadaBase):
    """Schema para crear datos procesados"""
    pass


class DataProcesadaResponse(DataProcesadaBase):
    """Schema para respuesta de datos procesados"""
    id: int
    
    @field_serializer('total_uf')
    def serialize_total_uf(self, value: float) -> float:
        return round(value, 2)
    
    @field_serializer('total_clp')
    def serialize_total_clp(self, value: float) -> int:
        return int(value)
    
    @field_serializer('cantidad_total')
    def serialize_cantidad_total(self, value: float) -> int:
        return int(value)
    
    @field_serializer('total_tonelada')
    def serialize_total_tonelada(self, value: float) -> float:
        return round(value, 5)
    
    @field_serializer('total_gramos')
    def serialize_total_gramos(self, value: float) -> float:
        return round(value, 5)
    
    class Config:
        from_attributes = True


class DataProcesadaUpdate(BaseModel):
    """Schema para actualizar datos procesados (todos los campos opcionales)"""
    codigo_interno: Optional[int] = None
    celda: Optional[str] = None
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None
    tipo_material: Optional[str] = None
    material: Optional[str] = None
    riesgo: Optional[str] = None
    total_tonelada: Optional[float] = None
    total_gramos: Optional[float] = None
    cantidad_total: Optional[float] = None
    total_uf: Optional[float] = None
    total_clp: Optional[float] = None
    periodo: Optional[str] = None
