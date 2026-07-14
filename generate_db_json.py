import json
import os
import re
import glob

ruta_tarifas = os.path.join("Parametros", "tarifas.json")
ruta_salida = "db.json"

with open(ruta_tarifas, "r", encoding="utf-8") as f:
    tarifas = json.load(f)

codigos_internos = [t["codigo"] for t in tarifas]

# Intentar leer ERPs reales desde el Excel de ventas si existe
erps_reales = []
excels = glob.glob("data/*.xlsx") + glob.glob("data/*.xls") + glob.glob("*.xlsx")
for ruta_excel in excels:
    try:
        import pandas as pd
        df = pd.read_excel(ruta_excel)
        if "codigo_erp" in df.columns:
            erps_raw = df["codigo_erp"].dropna().astype(str).unique()
            erps_reales = sorted(set(re.sub(r"[^0-9A-Za-z]+$", "", e).strip() for e in erps_raw if e.strip()))
            print(f"Leyendo {len(erps_reales)} ERPs únicos desde {ruta_excel}")
            break
    except Exception as ex:
        print(f"No se pudo leer {ruta_excel}: {ex}")

if not erps_reales:
    # Fallback: usar codigo_interno como codigo_erp (comportamiento original)
    erps_reales = [str(t["codigo"]) for t in tarifas]
    print(f"No se encontró Excel con codigo_erp. Usando {len(erps_reales)} códigos de tarifas.json.")

# Asignar codigo_interno ciclando sobre los disponibles en tarifas
# NOTA: Este es un mapeo placeholder. Reemplazar db.json con datos reales de MySQL (productos_erp).
productos = []
for i, erp in enumerate(erps_reales):
    codigo_interno = codigos_internos[i % len(codigos_internos)]
    productos.append({
        "codigo_erp": erp,
        "nombre": f"Producto {erp}",
        "peso_ton": 0.001,
        "peso_gr": 1.0,
        "codigo_interno": int(codigo_interno),
        "categoria": "Sin Categoria",
        "subcategoria": "Sin Subcategoria",
        "tipo_material": "Sin Tipo",
        "material": "Sin Material",
        "riesgo": "Bajo"
    })

with open(ruta_salida, "w", encoding="utf-8") as f:
    json.dump(productos, f, ensure_ascii=False, indent=4)

print(f"Se generaron {len(productos)} productos en {ruta_salida}")
print("ADVERTENCIA: El mapeo codigo_erp → codigo_interno es un placeholder.")
print("Reemplaza db.json con los datos reales de la tabla productos_erp de MySQL.")
