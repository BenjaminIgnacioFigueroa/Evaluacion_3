from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import DataModel
from schemas import DataCreate, DataResponse

router = APIRouter(prefix="/data", tags=["Datos"])


@router.post("/", response_model=DataResponse)
def create_data(data: DataCreate, db: Session = Depends(get_db)):
    """Crear un nuevo registro de datos"""
    db_data = DataModel(**data.model_dump())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


@router.get("/{data_id}", response_model=DataResponse)
def read_data(data_id: int, db: Session = Depends(get_db)):
    """Obtener un registro de datos por ID"""
    db_data = db.query(DataModel).filter(DataModel.id == data_id).first()
    if db_data is None:
        raise HTTPException(status_code=404, detail="Dato no encontrado")
    return db_data


@router.get("/", response_model=List[DataResponse])
def read_all_data(db: Session = Depends(get_db)):
    """Obtener todos los registros de datos"""
    return db.query(DataModel).all()
