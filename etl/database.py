from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from etl.config import settings

# Variables globales para la base de datos
engine = None
SessionLocal = None


def init_database():
    """Inicializar la conexión a la base de datos"""
    global engine, SessionLocal
    
    if not settings.DATABASE_URL:
        return False
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return True
    except Exception as e:
        print(f"Error conectando a PostgreSQL: {e}")
        return False


def get_db() -> Session:
    """Obtener sesión de base de datos"""
    if SessionLocal is None:
        raise Exception("Base de datos no configurada")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables(base):
    """Crear todas las tablas en la base de datos"""
    if engine:
        base.metadata.create_all(bind=engine)
