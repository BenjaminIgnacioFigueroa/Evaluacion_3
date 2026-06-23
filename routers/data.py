from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from typing import List, Optional
import pandas as pd
import json
import requests
import io
from etl.database import get_db
from etl.models import ProductoModel, VentaUnitariaModel, TarifaModel, CierreUFModel, DataProcesadaModel
from etl.schemas import ProductoCreate, ProductoResponse, ProductoUpdate, VentaUnitariaCreate, VentaUnitariaResponse, VentaUnitariaUpdate, VentaConProductoResponse, TarifaCreate, TarifaResponse, TarifaUpdate, VentaCompletaResponse, CierreUFCreate, CierreUFResponse, CierreUFUpdate, DataProcesadaCreate, DataProcesadaResponse, DataProcesadaUpdate

router = APIRouter(prefix="/productos", tags=["Productos"])

ventas_router = APIRouter(prefix="/ventas-unitarias", tags=["Ventas Unitarias"])

tarifas_router = APIRouter(prefix="/tarifas", tags=["Tarifas"])

cierres_uf_router = APIRouter(prefix="/cierres-uf", tags=["Cierres UF"])

data_procesada_router = APIRouter(prefix="/data-procesada", tags=["Data Procesada"])


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


# Endpoints para Cierres UF
@cierres_uf_router.post("/", response_model=CierreUFResponse)
def create_cierre_uf(cierre: CierreUFCreate, db: Session = Depends(get_db)):
    """Crear un nuevo cierre de UF"""
    db_cierre = CierreUFModel(**cierre.model_dump())
    db.add(db_cierre)
    db.commit()
    db.refresh(db_cierre)
    return db_cierre


@cierres_uf_router.get("/{cierre_id}", response_model=CierreUFResponse)
def read_cierre_uf(cierre_id: int, db: Session = Depends(get_db)):
    """Obtener un cierre de UF por ID"""
    db_cierre = db.query(CierreUFModel).filter(CierreUFModel.id == cierre_id).first()
    if db_cierre is None:
        raise HTTPException(status_code=404, detail="Cierre UF no encontrado")
    return db_cierre


@cierres_uf_router.get("/", response_model=List[CierreUFResponse])
def read_all_cierres_uf(db: Session = Depends(get_db)):
    """Obtener todos los cierres de UF"""
    return db.query(CierreUFModel).all()


@cierres_uf_router.get("/ciclo/{ciclo}", response_model=CierreUFResponse)
def read_cierre_uf_by_ciclo(ciclo: str, db: Session = Depends(get_db)):
    """Obtener un cierre de UF por ciclo"""
    db_cierre = db.query(CierreUFModel).filter(CierreUFModel.ciclo == ciclo).first()
    if db_cierre is None:
        raise HTTPException(status_code=404, detail="Cierre UF no encontrado para el ciclo")
    return db_cierre


@cierres_uf_router.put("/{cierre_id}", response_model=CierreUFResponse)
def update_cierre_uf(cierre_id: int, cierre: CierreUFUpdate, db: Session = Depends(get_db)):
    """Actualizar un cierre de UF existente"""
    db_cierre = db.query(CierreUFModel).filter(CierreUFModel.id == cierre_id).first()
    if db_cierre is None:
        raise HTTPException(status_code=404, detail="Cierre UF no encontrado")
    
    update_data = cierre.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cierre, field, value)
    
    db.commit()
    db.refresh(db_cierre)
    return db_cierre


@cierres_uf_router.delete("/{cierre_id}")
def delete_cierre_uf(cierre_id: int, db: Session = Depends(get_db)):
    """Eliminar un cierre de UF"""
    db_cierre = db.query(CierreUFModel).filter(CierreUFModel.id == cierre_id).first()
    if db_cierre is None:
        raise HTTPException(status_code=404, detail="Cierre UF no encontrado")
    
    db.delete(db_cierre)
    db.commit()
    return {"message": "Cierre UF eliminado correctamente"}


@cierres_uf_router.post("/importar-json")
async def importar_cierres_uf_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importar cierres de UF desde archivo JSON (cierreUF.json)"""
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un JSON")
    
    try:
        # Leer el archivo JSON
        content = await file.read()
        cierres_data = json.loads(content)
        
        # Validar que sea una lista
        if not isinstance(cierres_data, list):
            raise HTTPException(status_code=400, detail="El JSON debe contener una lista de cierres UF")
        
        # Procesar cada elemento
        registros_creados = 0
        errores = []
        
        for index, cierre_item in enumerate(cierres_data):
            try:
                # Validar campos requeridos (soportar CICLO o ciclo)
                ciclo = cierre_item.get('CICLO') or cierre_item.get('ciclo')
                uf_pesos = cierre_item.get('UFpesos') or cierre_item.get('uf_pesos')
                
                if not ciclo or uf_pesos is None:
                    errores.append(f"Elemento {index + 1}: Faltan campos requeridos (CICLO/ciclo y UFpesos/uf_pesos)")
                    continue
                
                cierre_data = {
                    'ciclo': str(ciclo),
                    'uf_pesos': float(uf_pesos)
                }
                
                # Upsert atómico para evitar race conditions
                stmt = insert(CierreUFModel).values(**cierre_data)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['ciclo'],
                    set_={'uf_pesos': stmt.excluded.uf_pesos}
                )
                db.execute(stmt)
                registros_creados += 1
            except Exception as e:
                errores.append(f"Elemento {index + 1}: {str(e)}")
        
        db.commit()
        
        return {
            "message": "Importación completada",
            "registros_procesados": registros_creados,
            "errores": errores if errores else None
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error al decodificar el archivo JSON")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")


@cierres_uf_router.post("/actualizar-desde-api")
async def actualizar_cierres_desde_api(anios: List[int] = [2025, 2026], db: Session = Depends(get_db)):
    """Actualizar cierres de UF consumiendo la API de miindicador.cl"""
    try:
        registros_creados = 0
        errores = []
        
        for anio in anios:
            try:
                url = f"https://mindicador.cl/api/uf/{anio}"
                resp = requests.get(url, timeout=20)
                resp.raise_for_status()
                data = resp.json()
                
                df = pd.DataFrame(data["serie"])
                df["fecha"] = pd.to_datetime(df["fecha"])
                df["fecha"] = df["fecha"].dt.tz_localize(None)
                
                # Obtener cierres de mes (último día de cada mes)
                cierres = df.groupby([df["fecha"].dt.year, df["fecha"].dt.month]).tail(1)
                
                for _, row in cierres.iterrows():
                    ciclo = row["fecha"].strftime("%Y%m")
                    uf_pesos = row["valor"]
                    
                    # Upsert atómico para evitar race conditions
                    cierre_data = {
                        'ciclo': ciclo,
                        'uf_pesos': float(uf_pesos)
                    }
                    stmt = insert(CierreUFModel).values(**cierre_data)
                    stmt = stmt.on_conflict_do_update(
                        index_elements=['ciclo'],
                        set_={'uf_pesos': stmt.excluded.uf_pesos}
                    )
                    db.execute(stmt)
                    registros_creados += 1
                        
            except Exception as e:
                errores.append(f"Año {anio}: {str(e)}")
        
        db.commit()
        
        return {
            "message": "Actualización desde API completada",
            "registros_procesados": registros_creados,
            "errores": errores if errores else None
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al consumir la API: {str(e)}")


# Endpoints para Data Procesada
@data_procesada_router.post("/procesar-todos")
def procesar_todos_ciclos(db: Session = Depends(get_db)):
    """Procesar datos para todos los ciclos disponibles en ventas_unitarias"""
    try:
        # Obtener todos los ciclos únicos de ventas unitarias
        ciclos = db.query(VentaUnitariaModel.ciclo).distinct().all()
        ciclos = [c[0] for c in ciclos]
        
        if not ciclos:
            raise HTTPException(status_code=404, detail="No se encontraron ciclos en ventas unitarias")
        
        resultados = []
        errores = []
        
        for ciclo in ciclos:
            try:
                # Obtener todas las ventas del ciclo
                ventas = db.query(VentaUnitariaModel).filter(VentaUnitariaModel.ciclo == ciclo).all()
                
                if not ventas:
                    errores.append(f"Ciclo {ciclo}: No se encontraron ventas")
                    continue
                
                # Obtener el valor de UF para el ciclo
                cierre_uf = db.query(CierreUFModel).filter(CierreUFModel.ciclo == ciclo).first()
                if not cierre_uf:
                    errores.append(f"Ciclo {ciclo}: No se encontró cierre UF")
                    continue
                
                valor_uf = cierre_uf.uf_pesos
                
                # Agrupar ventas por codigo_interno
                from collections import defaultdict
                ventas_por_codigo = defaultdict(lambda: {
                    'cantidad_total': 0.0,
                    'total_tonelada': 0.0,
                    'total_gramos': 0.0,
                    'total_uf': 0.0
                })
                
                for venta in ventas:
                    # Obtener producto
                    producto = db.query(ProductoModel).filter(ProductoModel.codigo_erp == venta.codigo_erp).first()
                    if not producto:
                        continue
                    
                    # Obtener tarifa
                    tarifa = db.query(TarifaModel).filter(TarifaModel.codigo == producto.codigo_interno).first()
                    if not tarifa:
                        continue
                    
                    # Determinar tarifa según año del ciclo
                    anio = int(ciclo[:4])
                    valor_tarifa = tarifa.t2025 if anio == 2025 else tarifa.t2026
                    
                    # Calcular valores
                    cantidad = venta.cantidad
                    toneladas = cantidad * producto.peso_ton
                    gramos = cantidad * producto.peso_gr
                    uf = toneladas * valor_tarifa
                    
                    # Acumular
                    ventas_por_codigo[producto.codigo_interno]['cantidad_total'] += cantidad
                    ventas_por_codigo[producto.codigo_interno]['total_tonelada'] += toneladas
                    ventas_por_codigo[producto.codigo_interno]['total_gramos'] += gramos
                    ventas_por_codigo[producto.codigo_interno]['total_uf'] += uf
                
                # Crear o actualizar registros procesados
                registros_procesados = 0
                for codigo_interno, datos in ventas_por_codigo.items():
                    # Obtener información del producto y tarifa
                    producto = db.query(ProductoModel).filter(ProductoModel.codigo_interno == codigo_interno).first()
                    tarifa = db.query(TarifaModel).filter(TarifaModel.codigo == codigo_interno).first()
                    
                    if not producto or not tarifa:
                        continue
                    
                    # Calcular total CLP
                    total_clp = datos['total_uf'] * valor_uf
                    
                    # Verificar si ya existe un registro para este codigo_interno y ciclo
                    existing = db.query(DataProcesadaModel).filter(
                        DataProcesadaModel.codigo_interno == codigo_interno,
                        DataProcesadaModel.periodo == ciclo
                    ).first()
                    
                    if existing:
                        # Actualizar registro existente
                        existing.celda = tarifa.celda
                        existing.categoria = producto.categoria
                        existing.subcategoria = producto.subcategoria
                        existing.tipo_material = producto.tipo_material
                        existing.material = producto.material
                        existing.riesgo = producto.riesgo
                        existing.total_tonelada = datos['total_tonelada']
                        existing.total_gramos = datos['total_gramos']
                        existing.cantidad_total = datos['cantidad_total']
                        existing.total_uf = datos['total_uf']
                        existing.total_clp = total_clp
                    else:
                        # Crear nuevo registro
                        data_procesada = DataProcesadaModel(
                            codigo_interno=codigo_interno,
                            celda=tarifa.celda,
                            categoria=producto.categoria,
                            subcategoria=producto.subcategoria,
                            tipo_material=producto.tipo_material,
                            material=producto.material,
                            riesgo=producto.riesgo,
                            total_tonelada=datos['total_tonelada'],
                            total_gramos=datos['total_gramos'],
                            cantidad_total=datos['cantidad_total'],
                            total_uf=datos['total_uf'],
                            total_clp=total_clp,
                            periodo=ciclo
                        )
                        db.add(data_procesada)
                    
                    registros_procesados += 1
                
                resultados.append({
                    "ciclo": ciclo,
                    "registros_procesados": registros_procesados,
                    "estado": "exitoso"
                })
                
            except Exception as e:
                errores.append(f"Ciclo {ciclo}: {str(e)}")
        
        db.commit()
        
        return {
            "message": "Procesamiento de todos los ciclos completado",
            "total_ciclos": len(ciclos),
            "ciclos_procesados": len(resultados),
            "resultados": resultados,
            "errores": errores if errores else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar todos los ciclos: {str(e)}")


@data_procesada_router.post("/procesar/{periodo}")
def procesar_datos(periodo: str, db: Session = Depends(get_db)):
    """Procesar datos para un periodo específico y generar registros en data_procesada (usando upsert para evitar duplicados)"""
    try:
        # Obtener todas las ventas del periodo
        ventas = db.query(VentaUnitariaModel).filter(VentaUnitariaModel.ciclo == periodo).all()
        
        if not ventas:
            raise HTTPException(status_code=404, detail=f"No se encontraron ventas para el periodo {periodo}")
        
        # Obtener el valor de UF para el periodo
        cierre_uf = db.query(CierreUFModel).filter(CierreUFModel.ciclo == periodo).first()
        if not cierre_uf:
            raise HTTPException(status_code=404, detail=f"No se encontró cierre UF para el periodo {periodo}")
        
        valor_uf = cierre_uf.uf_pesos
        
        # Agrupar ventas por codigo_interno
        from collections import defaultdict
        ventas_por_codigo = defaultdict(lambda: {
            'cantidad_total': 0.0,
            'total_tonelada': 0.0,
            'total_gramos': 0.0,
            'total_uf': 0.0
        })
        
        for venta in ventas:
            # Obtener producto
            producto = db.query(ProductoModel).filter(ProductoModel.codigo_erp == venta.codigo_erp).first()
            if not producto:
                continue
            
            # Obtener tarifa
            tarifa = db.query(TarifaModel).filter(TarifaModel.codigo == producto.codigo_interno).first()
            if not tarifa:
                continue
            
            # Determinar tarifa según año del periodo
            anio = int(periodo[:4])
            valor_tarifa = tarifa.t2025 if anio == 2025 else tarifa.t2026
            
            # Calcular valores
            cantidad = venta.cantidad
            toneladas = cantidad * producto.peso_ton
            gramos = cantidad * producto.peso_gr
            uf = toneladas * valor_tarifa
            
            # Acumular
            ventas_por_codigo[producto.codigo_interno]['cantidad_total'] += cantidad
            ventas_por_codigo[producto.codigo_interno]['total_tonelada'] += toneladas
            ventas_por_codigo[producto.codigo_interno]['total_gramos'] += gramos
            ventas_por_codigo[producto.codigo_interno]['total_uf'] += uf
        
        # Crear o actualizar registros procesados usando upsert (compatible con SQLite)
        registros_procesados = 0
        for codigo_interno, datos in ventas_por_codigo.items():
            # Obtener información del producto y tarifa
            producto = db.query(ProductoModel).filter(ProductoModel.codigo_interno == codigo_interno).first()
            tarifa = db.query(TarifaModel).filter(TarifaModel.codigo == codigo_interno).first()
            
            if not producto or not tarifa:
                continue
            
            # Calcular total CLP
            total_clp = datos['total_uf'] * valor_uf
            
            # Verificar si ya existe un registro para este codigo_interno y periodo
            existing = db.query(DataProcesadaModel).filter(
                DataProcesadaModel.codigo_interno == codigo_interno,
                DataProcesadaModel.periodo == periodo
            ).first()
            
            if existing:
                # Actualizar registro existente
                existing.celda = tarifa.celda
                existing.categoria = producto.categoria
                existing.subcategoria = producto.subcategoria
                existing.tipo_material = producto.tipo_material
                existing.material = producto.material
                existing.riesgo = producto.riesgo
                existing.total_tonelada = datos['total_tonelada']
                existing.total_gramos = datos['total_gramos']
                existing.cantidad_total = datos['cantidad_total']
                existing.total_uf = datos['total_uf']
                existing.total_clp = total_clp
            else:
                # Crear nuevo registro
                data_procesada = DataProcesadaModel(
                    codigo_interno=codigo_interno,
                    celda=tarifa.celda,
                    categoria=producto.categoria,
                    subcategoria=producto.subcategoria,
                    tipo_material=producto.tipo_material,
                    material=producto.material,
                    riesgo=producto.riesgo,
                    total_tonelada=datos['total_tonelada'],
                    total_gramos=datos['total_gramos'],
                    cantidad_total=datos['cantidad_total'],
                    total_uf=datos['total_uf'],
                    total_clp=total_clp,
                    periodo=periodo
                )
                db.add(data_procesada)
            
            registros_procesados += 1
        
        db.commit()
        
        return {
            "message": "Procesamiento completado",
            "periodo": periodo,
            "registros_procesados": registros_procesados
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar datos: {str(e)}")


@data_procesada_router.post("/", response_model=DataProcesadaResponse)
def create_data_procesada(data: DataProcesadaCreate, db: Session = Depends(get_db)):
    """Crear un nuevo registro de data procesada"""
    db_data = DataProcesadaModel(**data.model_dump())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


@data_procesada_router.get("/{data_id}", response_model=DataProcesadaResponse)
def read_data_procesada(data_id: int, db: Session = Depends(get_db)):
    """Obtener un registro de data procesada por ID"""
    db_data = db.query(DataProcesadaModel).filter(DataProcesadaModel.id == data_id).first()
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data procesada no encontrada")
    return db_data


@data_procesada_router.get("/", response_model=List[DataProcesadaResponse])
def read_all_data_procesada(db: Session = Depends(get_db)):
    """Obtener todos los registros de data procesada"""
    return db.query(DataProcesadaModel).all()


@data_procesada_router.get("/periodo/{periodo}", response_model=List[DataProcesadaResponse])
def read_data_procesada_by_periodo(periodo: str, db: Session = Depends(get_db)):
    """Obtener registros de data procesada por periodo"""
    return db.query(DataProcesadaModel).filter(DataProcesadaModel.periodo == periodo).all()


@data_procesada_router.get("/codigo/{codigo_interno}", response_model=List[DataProcesadaResponse])
def read_data_procesada_by_codigo(codigo_interno: int, db: Session = Depends(get_db)):
    """Obtener registros de data procesada por código interno"""
    return db.query(DataProcesadaModel).filter(DataProcesadaModel.codigo_interno == codigo_interno).all()


@data_procesada_router.put("/{data_id}", response_model=DataProcesadaResponse)
def update_data_procesada(data_id: int, data: DataProcesadaUpdate, db: Session = Depends(get_db)):
    """Actualizar un registro de data procesada existente"""
    db_data = db.query(DataProcesadaModel).filter(DataProcesadaModel.id == data_id).first()
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data procesada no encontrada")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_data, field, value)
    
    db.commit()
    db.refresh(db_data)
    return db_data


@data_procesada_router.delete("/{data_id}")
def delete_data_procesada(data_id: int, db: Session = Depends(get_db)):
    """Eliminar un registro de data procesada"""
    db_data = db.query(DataProcesadaModel).filter(DataProcesadaModel.id == data_id).first()
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data procesada no encontrada")
    
    db.delete(db_data)
    db.commit()
    return {"message": "Data procesada eliminada correctamente"}


@data_procesada_router.delete("/limpiar/todos")
def limpiar_toda_data_procesada(db: Session = Depends(get_db)):
    """Eliminar todos los registros de data procesada"""
    try:
        count = db.query(DataProcesadaModel).count()
        if count == 0:
            return {"message": "No hay datos procesados para eliminar", "registros_eliminados": 0}
        
        db.query(DataProcesadaModel).delete()
        db.commit()
        
        return {
            "message": "Todos los datos procesados han sido eliminados",
            "registros_eliminados": count
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar datos: {str(e)}")


@data_procesada_router.get("/descargar/excel")
def descargar_data_procesada_excel(periodo: Optional[str] = None, db: Session = Depends(get_db)):
    """Descargar data procesada en formato Excel"""
    query = db.query(DataProcesadaModel)
    
    if periodo:
        query = query.filter(DataProcesadaModel.periodo == periodo)
    
    datos = query.all()
    
    if not datos:
        raise HTTPException(status_code=404, detail="No se encontraron datos procesados")
    
    # Convertir a DataFrame
    df = pd.DataFrame([{
        'id': d.id,
        'codigo_interno': d.codigo_interno,
        'celda': d.celda,
        'categoria': d.categoria,
        'subcategoria': d.subcategoria,
        'tipo_material': d.tipo_material,
        'material': d.material,
        'riesgo': d.riesgo,
        'total_tonelada': round(d.total_tonelada, 5),
        'total_gramos': round(d.total_gramos, 5),
        'cantidad_total': int(d.cantidad_total),
        'total_uf': round(d.total_uf, 2),
        'total_clp': int(d.total_clp),
        'periodo': d.periodo
    } for d in datos])
    
    # Crear archivo Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data Procesada')
    output.seek(0)
    
    filename = f"data_procesada_{periodo if periodo else 'todos'}.xlsx"
    
    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )


@data_procesada_router.get("/descargar/csv")
def descargar_data_procesada_csv(periodo: Optional[str] = None, db: Session = Depends(get_db)):
    """Descargar data procesada en formato CSV"""
    query = db.query(DataProcesadaModel)
    
    if periodo:
        query = query.filter(DataProcesadaModel.periodo == periodo)
    
    datos = query.all()
    
    if not datos:
        raise HTTPException(status_code=404, detail="No se encontraron datos procesados")
    
    # Convertir a DataFrame
    df = pd.DataFrame([{
        'id': d.id,
        'codigo_interno': d.codigo_interno,
        'celda': d.celda,
        'categoria': d.categoria,
        'subcategoria': d.subcategoria,
        'tipo_material': d.tipo_material,
        'material': d.material,
        'riesgo': d.riesgo,
        'total_tonelada': round(d.total_tonelada, 5),
        'total_gramos': round(d.total_gramos, 5),
        'cantidad_total': int(d.cantidad_total),
        'total_uf': round(d.total_uf, 2),
        'total_clp': int(d.total_clp),
        'periodo': d.periodo
    } for d in datos])
    
    # Crear archivo CSV en memoria
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    filename = f"data_procesada_{periodo if periodo else 'todos'}.csv"
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )


@data_procesada_router.get("/descargar/todos/excel")
def descargar_todos_periodos_excel(db: Session = Depends(get_db)):
    """Descargar data procesada de todos los periodos en Excel (consolidado)"""
    datos = db.query(DataProcesadaModel).all()
    
    if not datos:
        raise HTTPException(status_code=404, detail="No se encontraron datos procesados")
    
    # Convertir a DataFrame con todos los datos
    df = pd.DataFrame([{
        'id': d.id,
        'codigo_interno': d.codigo_interno,
        'celda': d.celda,
        'categoria': d.categoria,
        'subcategoria': d.subcategoria,
        'tipo_material': d.tipo_material,
        'material': d.material,
        'riesgo': d.riesgo,
        'total_tonelada': round(d.total_tonelada, 5),
        'total_gramos': round(d.total_gramos, 5),
        'cantidad_total': int(d.cantidad_total),
        'total_uf': round(d.total_uf, 2),
        'total_clp': int(d.total_clp),
        'periodo': d.periodo
    } for d in datos])
    
    # Ordenar por periodo
    df = df.sort_values('periodo')
    
    # Crear archivo Excel en memoria
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename="data_procesada_todos_periodos.xlsx"'}
    )


@data_procesada_router.get("/descargar/todos/csv")
def descargar_todos_periodos_csv(db: Session = Depends(get_db)):
    """Descargar data procesada de todos los periodos en CSV consolidado"""
    datos = db.query(DataProcesadaModel).all()
    
    if not datos:
        raise HTTPException(status_code=404, detail="No se encontraron datos procesados")
    
    # Convertir a DataFrame
    df = pd.DataFrame([{
        'id': d.id,
        'codigo_interno': d.codigo_interno,
        'celda': d.celda,
        'categoria': d.categoria,
        'subcategoria': d.subcategoria,
        'tipo_material': d.tipo_material,
        'material': d.material,
        'riesgo': d.riesgo,
        'total_tonelada': round(d.total_tonelada, 5),
        'total_gramos': round(d.total_gramos, 5),
        'cantidad_total': int(d.cantidad_total),
        'total_uf': round(d.total_uf, 2),
        'total_clp': int(d.total_clp),
        'periodo': d.periodo
    } for d in datos])
    
    # Ordenar por periodo
    df = df.sort_values('periodo')
    
    # Crear archivo CSV en memoria
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="data_procesada_todos_periodos.csv"'}
    )
