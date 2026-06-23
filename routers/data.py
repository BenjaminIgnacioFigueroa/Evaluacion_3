from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import ProductoModel
from schemas import ProductoCreate, ProductoResponse, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["Productos"])


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
