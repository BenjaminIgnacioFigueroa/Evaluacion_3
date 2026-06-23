from fastapi import APIRouter
import numpy as np
from etl.schemas import AnalysisResponse

router = APIRouter(prefix="/analisis", tags=["Análisis"])


@router.get("/basico", response_model=AnalysisResponse)
def analisis_basico():
    """Endpoint de ejemplo para análisis básico"""
    datos = np.random.rand(10)
    return {
        "media": float(np.mean(datos)),
        "desviacion": float(np.std(datos)),
        "maximo": float(np.max(datos)),
        "minimo": float(np.min(datos)),
        "datos": datos.tolist()
    }
