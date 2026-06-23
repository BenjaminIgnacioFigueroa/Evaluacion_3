from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from database import get_db
from models import ProductoModel, VentaUnitariaModel
from schemas import ProductoCreate, ProductoResponse, ProductoUpdate, VentaUnitariaCreate, VentaUnitariaResponse, VentaUnitariaUpdate

router = APIRouter(prefix="/productos", tags=["Productos"])

ventas_router = APIRouter(prefix="/ventas-unitarias", tags=["Ventas Unitarias"])


@router.post("/", response_model=ProductoResponse)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo producto"""
    db_producto = ProductoModel(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


@router.get("/{producto_id}", response_model=ProductoResponse)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    """Obtener un producto por ID"""
    db_producto = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


@router.get("/codigo/{codigo_interno}", response_model=ProductoResponse)
def read_producto_by_codigo(codigo_interno: int, db: Session = Depends(get_db)):
    """Obtener un producto por código interno"""
    db_producto = db.query(ProductoModel).filter(ProductoModel.codigo_interno == codigo_interno).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


@router.get("/", response_model=List[ProductoResponse])
def read_all_productos(db: Session = Depends(get_db)):
    """Obtener todos los productos"""
    return db.query(ProductoModel).all()


@router.put("/{producto_id}", response_model=ProductoResponse)
def update_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    """Actualizar un producto existente"""
    db_producto = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = producto.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_producto, field, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto


@router.delete("/{producto_id}")
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    """Eliminar un producto"""
    db_producto = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_producto)
    db.commit()
    return {"message": "Producto eliminado correctamente"}


# Endpoints para Ventas Unitarias
@ventas_router.post("/", response_model=VentaUnitariaResponse)
def create_venta_unitaria(venta: VentaUnitariaCreate, db: Session = Depends(get_db)):
    """Crear un nuevo registro de venta unitaria"""
    db_venta = VentaUnitariaModel(**venta.model_dump())
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)
    return db_venta


@ventas_router.get("/{venta_id}", response_model=VentaUnitariaResponse)
def read_venta_unitaria(venta_id: int, db: Session = Depends(get_db)):
    """Obtener una venta unitaria por ID"""
    db_venta = db.query(VentaUnitariaModel).filter(VentaUnitariaModel.id == venta_id).first()
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta unitaria no encontrada")
    return db_venta


@ventas_router.get("/", response_model=List[VentaUnitariaResponse])
def read_all_ventas_unitarias(db: Session = Depends(get_db)):
    """Obtener todas las ventas unitarias"""
    return db.query(VentaUnitariaModel).all()


@ventas_router.get("/ciclo/{ciclo}", response_model=List[VentaUnitariaResponse])
def read_ventas_by_ciclo(ciclo: str, db: Session = Depends(get_db)):
    """Obtener ventas unitarias por ciclo (mes/año)"""
    return db.query(VentaUnitariaModel).filter(VentaUnitariaModel.ciclo == ciclo).all()


@ventas_router.get("/producto/{codigo_erp}", response_model=List[VentaUnitariaResponse])
def read_ventas_by_producto(codigo_erp: str, db: Session = Depends(get_db)):
    """Obtener ventas unitarias por código de producto"""
    return db.query(VentaUnitariaModel).filter(VentaUnitariaModel.codigo_erp == codigo_erp).all()


@ventas_router.put("/{venta_id}", response_model=VentaUnitariaResponse)
def update_venta_unitaria(venta_id: int, venta: VentaUnitariaUpdate, db: Session = Depends(get_db)):
    """Actualizar una venta unitaria existente"""
    db_venta = db.query(VentaUnitariaModel).filter(VentaUnitariaModel.id == venta_id).first()
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta unitaria no encontrada")
    
    update_data = venta.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_venta, field, value)
    
    db.commit()
    db.refresh(db_venta)
    return db_venta


@ventas_router.delete("/{venta_id}")
def delete_venta_unitaria(venta_id: int, db: Session = Depends(get_db)):
    """Eliminar una venta unitaria"""
    db_venta = db.query(VentaUnitariaModel).filter(VentaUnitariaModel.id == venta_id).first()
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta unitaria no encontrada")
    
    db.delete(db_venta)
    db.commit()
    return {"message": "Venta unitaria eliminada correctamente"}


@ventas_router.post("/importar-excel")
async def importar_ventas_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importar ventas unitarias desde archivo Excel (VentaUnitaria.xlsx)"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx o .xls)")
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(file.file)
        
        # Validar columnas requeridas
        columnas_requeridas = ['ciclo', 'codigo_erp', 'cantidad']
        columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
        if columnas_faltantes:
            raise HTTPException(
                status_code=400, 
                detail=f"Faltan columnas requeridas: {', '.join(columnas_faltantes)}"
            )
        
        # Procesar cada fila
        registros_creados = 0
        errores = []
        
        for index, row in df.iterrows():
            try:
                venta_data = {
                    'ciclo': str(row['ciclo']),
                    'codigo_erp': str(row['codigo_erp']),
                    'cantidad': float(row['cantidad'])
                }
                
                db_venta = VentaUnitariaModel(**venta_data)
                db.add(db_venta)
                registros_creados += 1
            except Exception as e:
                errores.append(f"Fila {index + 1}: {str(e)}")
        
        db.commit()
        
        return {
            "message": "Importación completada",
            "registros_creados": registros_creados,
            "errores": errores if errores else None
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
