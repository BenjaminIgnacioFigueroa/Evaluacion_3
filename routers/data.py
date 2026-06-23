from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import json
from database import get_db
from models import ProductoModel, VentaUnitariaModel, TarifaModel
from schemas import ProductoCreate, ProductoResponse, ProductoUpdate, VentaUnitariaCreate, VentaUnitariaResponse, VentaUnitariaUpdate, VentaConProductoResponse, TarifaCreate, TarifaResponse, TarifaUpdate, VentaCompletaResponse

router = APIRouter(prefix="/productos", tags=["Productos"])

ventas_router = APIRouter(prefix="/ventas-unitarias", tags=["Ventas Unitarias"])

tarifas_router = APIRouter(prefix="/tarifas", tags=["Tarifas"])


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


@ventas_router.get("/join-producto/{ciclo}", response_model=List[VentaConProductoResponse])
def get_ventas_con_producto_por_ciclo(ciclo: str, db: Session = Depends(get_db)):
    """Obtener ventas unitarias con información del producto filtradas por ciclo"""
    # Realizar join entre VentaUnitaria y ProductoModel
    resultados = db.query(VentaUnitariaModel, ProductoModel).join(
        ProductoModel, 
        VentaUnitariaModel.codigo_erp == ProductoModel.codigo_erp
    ).filter(
        VentaUnitariaModel.ciclo == ciclo
    ).all()
    
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No se encontraron ventas para el ciclo {ciclo}")
    
    # Construir respuesta combinada
    respuesta = []
    for venta, producto in resultados:
        respuesta.append({
            "id": venta.id,
            "ciclo": venta.ciclo,
            "codigo_erp": venta.codigo_erp,
            "cantidad": venta.cantidad,
            "producto_nombre": producto.nombre,
            "producto_peso_ton": producto.peso_ton,
            "producto_peso_gr": producto.peso_gr,
            "producto_codigo_interno": producto.codigo_interno,
            "producto_categoria": producto.categoria,
            "producto_subcategoria": producto.subcategoria,
            "producto_tipo_material": producto.tipo_material,
            "producto_material": producto.material,
            "producto_riesgo": producto.riesgo
        })
    
    return respuesta


@ventas_router.get("/join-completo/{ciclo}", response_model=List[VentaCompletaResponse])
def get_ventas_completas_por_ciclo(ciclo: str, db: Session = Depends(get_db)):
    """Obtener ventas unitarias con información de producto y tarifa filtradas por ciclo"""
    # Realizar join triple: VentaUnitaria -> ProductoModel -> TarifaModel
    resultados = db.query(VentaUnitariaModel, ProductoModel, TarifaModel).join(
        ProductoModel, 
        VentaUnitariaModel.codigo_erp == ProductoModel.codigo_erp
    ).join(
        TarifaModel,
        ProductoModel.codigo_interno == TarifaModel.codigo
    ).filter(
        VentaUnitariaModel.ciclo == ciclo
    ).all()
    
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No se encontraron ventas para el ciclo {ciclo}")
    
    # Construir respuesta combinada
    respuesta = []
    for venta, producto, tarifa in resultados:
        respuesta.append({
            "id": venta.id,
            "ciclo": venta.ciclo,
            "codigo_erp": venta.codigo_erp,
            "cantidad": venta.cantidad,
            "producto_nombre": producto.nombre,
            "producto_peso_ton": producto.peso_ton,
            "producto_peso_gr": producto.peso_gr,
            "producto_codigo_interno": producto.codigo_interno,
            "producto_categoria": producto.categoria,
            "producto_subcategoria": producto.subcategoria,
            "producto_tipo_material": producto.tipo_material,
            "producto_material": producto.material,
            "producto_riesgo": producto.riesgo,
            "tarifa_celda": tarifa.celda,
            "tarifa_t2025": tarifa.t2025,
            "tarifa_t2026": tarifa.t2026
        })
    
    return respuesta


# Endpoints para Tarifas
@tarifas_router.post("/", response_model=TarifaResponse)
def create_tarifa(tarifa: TarifaCreate, db: Session = Depends(get_db)):
    """Crear una nueva tarifa"""
    db_tarifa = TarifaModel(**tarifa.model_dump())
    db.add(db_tarifa)
    db.commit()
    db.refresh(db_tarifa)
    return db_tarifa


@tarifas_router.get("/{tarifa_id}", response_model=TarifaResponse)
def read_tarifa(tarifa_id: int, db: Session = Depends(get_db)):
    """Obtener una tarifa por ID"""
    db_tarifa = db.query(TarifaModel).filter(TarifaModel.id == tarifa_id).first()
    if db_tarifa is None:
        raise HTTPException(status_code=404, detail="Tarifa no encontrada")
    return db_tarifa


@tarifas_router.get("/", response_model=List[TarifaResponse])
def read_all_tarifas(db: Session = Depends(get_db)):
    """Obtener todas las tarifas"""
    return db.query(TarifaModel).all()


@tarifas_router.get("/codigo/{codigo}", response_model=TarifaResponse)
def read_tarifa_by_codigo(codigo: int, db: Session = Depends(get_db)):
    """Obtener una tarifa por código"""
    db_tarifa = db.query(TarifaModel).filter(TarifaModel.codigo == codigo).first()
    if db_tarifa is None:
        raise HTTPException(status_code=404, detail="Tarifa no encontrada")
    return db_tarifa


@tarifas_router.put("/{tarifa_id}", response_model=TarifaResponse)
def update_tarifa(tarifa_id: int, tarifa: TarifaUpdate, db: Session = Depends(get_db)):
    """Actualizar una tarifa existente"""
    db_tarifa = db.query(TarifaModel).filter(TarifaModel.id == tarifa_id).first()
    if db_tarifa is None:
        raise HTTPException(status_code=404, detail="Tarifa no encontrada")
    
    update_data = tarifa.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tarifa, field, value)
    
    db.commit()
    db.refresh(db_tarifa)
    return db_tarifa


@tarifas_router.delete("/{tarifa_id}")
def delete_tarifa(tarifa_id: int, db: Session = Depends(get_db)):
    """Eliminar una tarifa"""
    db_tarifa = db.query(TarifaModel).filter(TarifaModel.id == tarifa_id).first()
    if db_tarifa is None:
        raise HTTPException(status_code=404, detail="Tarifa no encontrada")
    
    db.delete(db_tarifa)
    db.commit()
    return {"message": "Tarifa eliminada correctamente"}


@tarifas_router.post("/importar-json")
async def importar_tarifas_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importar tarifas desde archivo JSON (tarifas.json)"""
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un JSON")
    
    try:
        # Leer el archivo JSON
        content = await file.read()
        tarifas_data = json.loads(content)
        
        # Validar que sea una lista
        if not isinstance(tarifas_data, list):
            raise HTTPException(status_code=400, detail="El JSON debe contener una lista de tarifas")
        
        # Procesar cada elemento
        registros_creados = 0
        errores = []
        
        for index, tarifa_item in enumerate(tarifas_data):
            try:
                # Validar campos requeridos
                campos_requeridos = ['codigo', 'celda', 't2025', 't2026']
                campos_faltantes = [campo for campo in campos_requeridos if campo not in tarifa_item]
                if campos_faltantes:
                    errores.append(f"Elemento {index + 1}: Faltan campos requeridos: {', '.join(campos_faltantes)}")
                    continue
                
                tarifa_data = {
                    'codigo': int(tarifa_item['codigo']),
                    'celda': str(tarifa_item['celda']),
                    't2025': float(tarifa_item['t2025']),
                    't2026': float(tarifa_item['t2026'])
                }
                
                db_tarifa = TarifaModel(**tarifa_data)
                db.add(db_tarifa)
                registros_creados += 1
            except Exception as e:
                errores.append(f"Elemento {index + 1}: {str(e)}")
        
        db.commit()
        
        return {
            "message": "Importación completada",
            "registros_creados": registros_creados,
            "errores": errores if errores else None
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error al decodificar el archivo JSON")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
