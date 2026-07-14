import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from etl.config import settings
from etl.models import ProductoModel, TarifaModel, CierreUFModel, Base

# Crear engine y SessionLocal directamente
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    # --- Productos ---
    if not os.path.exists('db.json'):
        print("⚠️  No se encontró db.json. Saltando poblado inicial de productos.")
        print("   Puedes generarlo con: python generate_db_json.py")
    else:
        with open('db.json', 'r', encoding='utf-8') as f:
            productos_data = json.load(f)
        db.query(ProductoModel).delete()
        db.commit()
        count = 0
        for producto_data in productos_data:
            producto = ProductoModel(**producto_data)
            db.add(producto)
            count += 1
        db.commit()
        print(f"✅ Se insertaron {count} productos en la base de datos")

    # --- Tarifas ---
    ruta_tarifas = os.path.join('Parametros', 'tarifas.json')
    if not os.path.exists(ruta_tarifas):
        print("⚠️  No se encontró Parametros/tarifas.json. Saltando tarifas.")
    else:
        with open(ruta_tarifas, 'r', encoding='utf-8') as f:
            tarifas_data = json.load(f)
        count = 0
        for item in tarifas_data:
            codigo = int(item['codigo'])
            existing = db.query(TarifaModel).filter(TarifaModel.codigo == codigo).first()
            if existing:
                existing.celda = str(item['celda'])
                existing.t2025 = float(item['t2025'])
                existing.t2026 = float(item['t2026'])
            else:
                db.add(TarifaModel(
                    codigo=codigo,
                    celda=str(item['celda']),
                    t2025=float(item['t2025']),
                    t2026=float(item['t2026'])
                ))
                count += 1
        db.commit()
        print(f"✅ Se insertaron/actualizaron tarifas en la base de datos ({count} nuevas)")

    # --- Cierres UF ---
    ruta_cierre = os.path.join('Parametros', 'cierreUF.json')
    if not os.path.exists(ruta_cierre):
        print("⚠️  No se encontró Parametros/cierreUF.json. Saltando cierres UF.")
    else:
        with open(ruta_cierre, 'r', encoding='utf-8') as f:
            cierres_data = json.load(f)
        count = 0
        for item in cierres_data:
            ciclo = str(item.get('CICLO') or item.get('ciclo', ''))
            uf_pesos = item.get('UFpesos') or item.get('uf_pesos')
            if not ciclo or uf_pesos is None:
                continue
            existing = db.query(CierreUFModel).filter(CierreUFModel.ciclo == ciclo).first()
            if existing:
                existing.uf_pesos = float(uf_pesos)
            else:
                db.add(CierreUFModel(ciclo=ciclo, uf_pesos=float(uf_pesos)))
                count += 1
        db.commit()
        print(f"✅ Se insertaron/actualizaron cierres UF en la base de datos ({count} nuevos)")

except Exception as e:
    db.rollback()
    print(f"❌ Error al insertar datos: {e}")
finally:
    db.close()
