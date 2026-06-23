import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from models import ProductoModel, Base

# Crear engine y SessionLocal directamente
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Cargar datos del JSON
with open('db.json', 'r', encoding='utf-8') as f:
    productos_data = json.load(f)

# Insertar datos en la base de datos
db = SessionLocal()
try:
    count = 0
    for producto_data in productos_data:
        # Verificar si el producto ya existe por codigo_erp
        existing = db.query(ProductoModel).filter(
            ProductoModel.codigo_erp == producto_data['codigo_erp']
        ).first()
        
        if not existing:
            producto = ProductoModel(**producto_data)
            db.add(producto)
            count += 1
    
    db.commit()
    print(f"✅ Se insertaron {count} productos en la base de datos")
except Exception as e:
    db.rollback()
    print(f"❌ Error al insertar datos: {e}")
finally:
    db.close()
