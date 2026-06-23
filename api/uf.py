import requests
import pandas as pd
import json
import os

def uf_cierres_mes(anios=[2025, 2026], carpeta="Parametros"):
    frames = []
    for anio in anios:
        url = f"https://mindicador.cl/api/uf/{anio}"
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        df = pd.DataFrame(data["serie"])
        df["fecha"] = pd.to_datetime(df["fecha"])
        df["fecha"] = df["fecha"].dt.tz_localize(None)
        frames.append(df)

    df = pd.concat(frames)
    df = df.sort_values("fecha")

    cierres = df.groupby([df["fecha"].dt.year, df["fecha"].dt.month]).tail(1)

    valores_json = []
    for _, row in cierres.iterrows():
        ciclo = row["fecha"].strftime("%Y%m")
        valores_json.append({
            "CICLO": ciclo,
            "UFpesos": row["valor"]
        })

    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, "cierreUF.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(valores_json, f, ensure_ascii=False, indent=4)

    print(f"Archivo guardado en: {os.path.abspath(ruta)}")

if __name__ == "__main__":
    uf_cierres_mes()