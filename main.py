from fastapi import FastAPI
from config import settings
from database import init_database, create_tables
from models import Base
from routers import analysis, data, health

# Inicializar base de datos
db_connected = init_database()
if db_connected:
    create_tables(Base)

# Inicializar FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Registrar routers
app.include_router(analysis.router)
app.include_router(data.router)
app.include_router(data.ventas_router)
app.include_router(health.router)


@app.get("/")
def read_root():
    return {
        "message": settings.APP_NAME,
        "documentacion": "/docs",
        "version": settings.APP_VERSION
    }


@app.on_event("startup")
def startup_event():
    print("\n" + "="*60)
    print("🚀 API de Ciencia de Datos iniciada")
    print("="*60)
    print("📚 Documentación Swagger: http://localhost:8000/docs")
    print("📖 Documentación ReDoc:  http://localhost:8000/redoc")
    print("🏥 Health Check:         http://localhost:8000/health")
    print("="*60)
    if db_connected:
        print("✅ Base de datos conectada")
    else:
        print("⚠️  Base de datos no configurada")
    print("="*60 + "\n")
