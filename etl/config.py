import os
from typing import Optional


class Settings:
    """Configuración de la aplicación"""
    
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", "sqlite:///./data_science.db")
    APP_NAME: str = "API de Ciencia de Datos"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API para análisis de datos con FastAPI"


settings = Settings()
