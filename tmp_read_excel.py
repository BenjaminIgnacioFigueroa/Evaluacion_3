import pandas as pd
import json

df = pd.read_excel(r"c:\Users\emmanuel.chavero\Videos\Captures\Evaluacion_3\data\ventaUnitaria.xlsx")
print("Columnas:", df.columns.tolist())
print("Total filas:", len(df))
print("Primeras filas:")
print(df.head(10).to_string(index=False))
print("\nCodigos ERP unicos (primeros 30):")
print(json.dumps(df['codigo_erp'].unique()[:30].tolist(), indent=2))
