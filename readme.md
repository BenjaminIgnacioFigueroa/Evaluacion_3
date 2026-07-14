# Sistema de Análisis de Datos de Reciclaje - Informe Ejecutivo

## 1. Resumen Ejecutivo

Este proyecto implementa un sistema integral de análisis de datos para el procesamiento de información de ventas de productos de reciclaje. El sistema combina una API REST desarrollada en FastAPI (Python) con un dashboard interactivo en React, permitiendo el cálculo automatizado de tarifas, conversión de unidades monetarias (UF a CLP) y generación de reportes ejecutivos.

**Objetivo Principal:** Automatizar el procesamiento de datos de ventas unitarias, calcular totales en toneladas y gramos, aplicar tarifas por producto, y convertir valores a pesos chilenos utilizando el valor de cierre de la UF.

**Tecnologías:**
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** React 19, Vite, Recharts, TailwindCSS
- **Base de Datos:** SQLite (configurable para MySQL/PostgreSQL)

---

## 2. Arquitectura del Sistema

### 2.1 Estructura de Datos

El sistema procesa información desde múltiples fuentes de datos:

#### **Data 1: VentaUnitaria.xlsx**
- **Origen:** Área comercial (facturación mensual)
- **Periodo:** Enero 2025 - Abril 2026
- **Columnas:**
  - `ciclo`: Mes y año de la venta (formato: YYYY-MM)
  - `codigo_erp`: Código del producto vendido (FK con productos_erp)
  - `cantidad`: Total vendido por producto en el mes/año correspondiente

#### **Data 2: productos_erp (Base de Datos)**
- **Origen:** Base de datos MySQL
- **Columnas:**
  - `codigo_erp`: Identificador único del producto
  - `nombre`: Nombre descriptivo del producto
  - `peso_ton`: Peso en toneladas
  - `peso_gr`: Peso en gramos
  - `codigo_interno`: Código interno para unión con tarifas
  - `categoria`: Categoría del producto
  - `subcategoria`: Subcategoría del producto
  - `tipo_material`: Tipo de material
  - `material`: Material específico
  - `riesgo`: Nivel de riesgo

**Relación:** `ventaUnitaria.codigo_erp = productos.codigo_erp`

#### **Data 3: tarifas.json**
- **Ubicación:** `Parametros/tarifas.json`
- **Columnas:**
  - `codigo`: Código para unión con `productos.codigo_interno`
  - `celda`: Identificador de celda en Excel para reporte final
  - `t2025`: Tarifa en UF/tonelada para año 2025
  - `t2026`: Tarifa en UF/tonelada para año 2026

**Relación:** `productos.codigo_interno = tarifas.codigo`

#### **Data 4: cierreUF.json**
- **Ubicación:** `Parametros/cierreUF.json`
- **Origen:** API miindicador.cl (backup manual desde SII)
- **Contenido:** Valor de cierre de UF por periodo

#### **Data 5: data_procesada (Base de Datos)**
- **Propósito:** Almacenar resultados del procesamiento
- **Columnas:**
  - `codigo_interno`: Código interno del producto
  - `celda`: Celda de reporte (desde tarifas)
  - `categoria`: Categoría del producto
  - `subcategoria`: Subcategoría del producto
  - `tipo_material`: Tipo de material
  - `material`: Material específico
  - `riesgo`: Nivel de riesgo
  - `total_tonelada`: Suma de `cantidad × peso_ton` por código interno
  - `total_gramos`: Suma de `cantidad × peso_gr` por código interno
  - `cantidad_total`: Cantidad total de productos vendidos por código interno
  - `total_uf`: Suma total en UF de productos vendidos
  - `total_clp`: `total_uf × valor_cierre_uf` según periodo
  - `periodo`: Periodo de totalización (formato YYYYMM)

### 2.2 Flujo de Procesamiento

```
VentaUnitaria.xlsx → productos_erp → tarifas.json → cierreUF.json → data_procesada
        ↓                  ↓              ↓              ↓              ↓
   [Cargar Datos]   [Unión ERP]   [Aplicar Tarifas] [Convertir UF]   [Guardar Resultados]
```

---

## 3. Requisitos Previos

### 3.1 Software Requerido
- **Python 3.10+** (recomendado: 3.11)
- **Node.js 18+** y npm
- **Git** (para control de versiones)

**Opcional para despliegue con contenedores:**
- **Docker Engine 24+**
- **Docker Compose 2.20+**
- **Ubuntu/WSL2** si se ejecuta en Windows sin Docker Desktop

### 3.2 Archivos de Configuración Requeridos
- `db.json`: Archivo con datos de productos para poblado inicial
- `Parametros/tarifas.json`: Configuración de tarifas por producto
- `Parametros/cierreUF.json`: Valores de cierre de UF por periodo
- `DataMysql.xlsx`: Datos de ventas unitarias (opcional, según implementación)

---

## 4. Guía de Instalación y Configuración

### 4.1 Clonación del Proyecto

```bash
git clone <repository-url>
cd Evaluacion_3
```

### 4.2 Configuración del Entorno Virtual (Backend)

#### Paso 1: Crear entorno virtual
```bash
python -m venv venv
```

#### Paso 2: Activar entorno virtual

**En Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**En Linux/Mac:**
```bash
source venv/bin/activate
```

**Verificación:** El prompt debería mostrar `(venv)` al inicio.

#### Paso 3: Instalar dependencias de Python

Crear archivo `requirements.txt` si no existe:
```bash
pip install fastapi uvicorn sqlalchemy python-multipart
```

O instalar desde requirements.txt (si existe):
```bash
pip install -r requirements.txt
```

### 4.3 Configuración del Frontend

#### Paso 1: Navegar al directorio del dashboard
```bash
cd dashboards
```

#### Paso 2: Instalar dependencias de Node.js
```bash
npm install
```

#### Paso 3: Volver al directorio raíz
```bash
cd ..
```

### 4.4 Configuración de Variables de Entorno

Crear archivo `.env` en el directorio raíz:
```env
DATABASE_URL=sqlite:///./data_science.db
```

**Nota:** Para producción, configurar con PostgreSQL o MySQL:
```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/nombre_db
# o
DATABASE_URL=mysql://usuario:password@localhost:3306/nombre_db
```

---

### 4.5 Despliegue con Docker (Opcional)

Esta sección permite levantar todo el sistema mediante contenedores, sin instalar Python ni Node.js localmente. Está diseñada para ejecutarse dentro de **Ubuntu/WSL2** en Windows.

#### 4.5.1 Instalar Docker en Ubuntu/WSL2

```bash
sudo apt update
sudo apt install docker.io docker-compose-v2
sudo service docker start
sudo usermod -aG docker $USER
```

**Nota:** Si `newgrp docker` no está disponible, instálalo con:
```bash
sudo apt install util-linux-extra
newgrp docker
```

Cierra y vuelve a abrir la terminal para aplicar los cambios de grupo, o ejecuta `newgrp docker` en la sesión actual.

#### 4.5.2 Archivos de Dockerización

El repositorio incluye los siguientes archivos en la raíz:

- `Dockerfile.backend`: Imagen del backend FastAPI.
- `Dockerfile.frontend`: Imagen del frontend React + Vite.
- `docker-compose.yml`: Orquestación de ambos servicios.
- `.dockerignore`: Archivos excluidos de la imagen.
- `requirements.txt`: Dependencias Python del backend.
- `generate_db_json.py`: Script auxiliar para generar `db.json` desde `Parametros/tarifas.json`.

#### 4.5.3 Generar base de datos inicial

No es necesario ejecutar nada manualmente. Al levantar el contenedor, el backend ejecuta automáticamente:

1. `generate_db_json.py` — lee los códigos ERP únicos desde `data/ventaUnitaria.xlsx` y genera `db.json` con un mapeo placeholder hacia los códigos internos de `tarifas.json`.
2. `seed_database.py` — limpia y recarga los productos, tarifas y cierres UF en la base de datos.

> **Nota sobre el mapeo ERP → código interno:** `generate_db_json.py` asigna códigos internos ciclando sobre `tarifas.json` como placeholder. Para obtener el mapeo real, exporta la tabla `productos_erp` desde MySQL y reemplaza `db.json` con el formato `{codigo_erp, nombre, peso_ton, peso_gr, codigo_interno, categoria, subcategoria, tipo_material, material, riesgo}`.

#### 4.5.4 Construir y levantar los contenedores

```bash
docker compose up --build
```

La primera vez descarga las imágenes base y construye el proyecto.

#### 4.5.5 Acceso a la aplicación

Una vez iniciados los contenedores:

- **Dashboard:** http://localhost:5173
- **API Swagger:** http://localhost:8000/docs
- **API ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

#### 4.5.6 Detener los contenedores

```bash
docker compose down
```

Para volver a levantar sin reconstruir imágenes:
```bash
docker compose up
```

---

## 5. Poblado de la Base de Datos

### 5.1 Verificar Archivo de Datos

Asegúrese de que el archivo `db.json` exista en el directorio raíz con la estructura de productos.

Si el archivo no existe, puede generarlo a partir de `Parametros/tarifas.json` ejecutando:

```bash
python generate_db_json.py
```

Este script lee los códigos ERP únicos desde `data/ventaUnitaria.xlsx` (si existe) y genera un producto por cada uno, asignando un `codigo_interno` de `tarifas.json` como placeholder. Si no encuentra el Excel, usa los códigos de `tarifas.json` como fallback.

> **Importante:** El mapeo `codigo_erp → codigo_interno` es un placeholder. Para resultados correctos, reemplaza `db.json` con los datos reales exportados desde la tabla `productos_erp` de MySQL.

### 5.2 Ejecutar Script de Poblado

Con el entorno virtual activado:
```bash
python seed_database.py
```

**Salida esperada:**
```
✅ Se insertaron X productos en la base de datos
```

**En caso de error:**
- Verificar que `db.json` existe y tiene formato JSON válido
- Verificar conexión a base de datos en `config.py`

### 5.3 Estructura de Tablas Creadas

El script crea automáticamente las siguientes tablas en SQLite:
- `productos`: Catálogo de productos ERP
- `ventas_unitarias`: Ventas mensuales por producto
- `tarifas`: Tarifas por producto y año
- `cierres_uf`: Valores de cierre de UF por periodo
- `data_procesada`: Resultados procesados

---

## 6. Ejecución del Sistema

### 6.1 Iniciar Backend (API FastAPI)

Con el entorno virtual activado:
```bash
uvicorn etl.main:app --reload --host 0.0.0.0 --port 8000
```

**Opciones adicionales:**
- `--reload`: Recarga automática al detectar cambios (desarrollo)
- `--host 0.0.0.0`: Accesible desde la red
- `--port 8000`: Puerto de escucha (configurable)

**Salida esperada:**
```
============================================================
🚀 API de Ciencia de Datos iniciada
============================================================
📚 Documentación Swagger: http://localhost:8000/docs
📖 Documentación ReDoc:  http://localhost:8000/redoc
🏥 Health Check:         http://localhost:8000/health
============================================================
✅ Base de datos conectada
============================================================
```

### 6.2 Iniciar Frontend (Dashboard React)

En una nueva terminal (manteniendo el backend activo):

```bash
cd dashboards
npm run dev
```

**Salida esperada:**
```
  VITE v8.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 6.3 Acceso a la Aplicación

- **Dashboard:** http://localhost:5173
- **API Swagger:** http://localhost:8000/docs
- **API ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 7. Endpoints de la API

### 7.1 Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información general de la API |
| GET | `/health` | Estado de salud del sistema |
| GET | `/docs` | Documentación interactiva Swagger |
| GET | `/redoc` | Documentación ReDoc |

### 7.2 Endpoints de Datos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/productos` | Listar todos los productos |
| POST | `/api/productos` | Crear nuevo producto |
| GET | `/api/ventas` | Listar ventas unitarias |
| POST | `/api/ventas` | Cargar ventas desde Excel |
| GET | `/api/tarifas` | Listar tarifas |
| POST | `/api/tarifas` | Cargar tarifas desde JSON |
| GET | `/api/cierres-uf` | Listar cierres de UF |
| POST | `/api/cierres-uf` | Actualizar cierres de UF |
| GET | `/api/data-procesada` | Listar datos procesados |
| POST | `/api/analysis/process` | Ejecutar procesamiento de datos |

### 7.3 Documentación Interactiva

La API incluye documentación automática via Swagger UI:
1. Navegar a http://localhost:8000/docs
2. Explorar endpoints disponibles
3. Probar endpoints directamente desde la interfaz

---

## 8. Flujo de Trabajo Recomendado

### 8.1 Primer Despliegue

1. **Configurar entorno:**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   pip install fastapi uvicorn sqlalchemy
   ```

2. **Poblar base de datos:**
   ```bash
   python seed_database.py
   ```

3. **Iniciar backend:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Iniciar frontend (nueva terminal):**
   ```bash
   cd dashboards
   npm install
   npm run dev
   ```

5. **Verificar funcionamiento:**
   - Acceder a http://localhost:5173
   - Verificar http://localhost:8000/health
   - Explorar http://localhost:8000/docs

### 8.2 Desarrollo Iterativo

1. **Modificar código backend** → Recarga automática con `--reload`
2. **Modificar código frontend** → Recarga automática con Vite
3. **Verificar cambios** en el navegador
4. **Probar API** via Swagger UI

### 8.3 Actualización de Datos

1. **Actualizar ventas:**
   - Reemplazar `data/ventaUnitaria.xlsx`
   - Usar endpoint `POST /ventas-unitarias/importar-excel` para cargar

2. **Actualizar tarifas:**
   - Modificar `Parametros/tarifas.json`
   - Usar endpoint `POST /tarifas/importar-json` para recargar

3. **Actualizar cierres UF:**
   - Modificar `Parametros/cierreUF.json`
   - Usar endpoint `POST /cierres-uf/importar-json` para recargar
   - Alternativa: usar `POST /cierres-uf/actualizar-desde-api` con body `[2025, 2026]`

4. **Reprocesar datos:**
   - Ejecutar `POST /data-procesada/procesar-todos`
   - O ejecutar `POST /data-procesada/procesar/{periodo}` para un periodo específico

### 8.4 Flujo de Carga Inicial Completo (Docker)

Antes de procesar datos por primera vez, asegúrate de tener cargados los siguientes elementos:

1. **Productos**: generados automáticamente desde `db.json` al levantar el contenedor.
2. **Tarifas**: subir `Parametros/tarifas.json` vía `POST /tarifas/importar-json`.
3. **Cierres UF**: subir `Parametros/cierreUF.json` vía `POST /cierres-uf/importar-json`, o consumir la API de miindicador.cl con `POST /cierres-uf/actualizar-desde-api`.
4. **Ventas unitarias**: subir `data/ventaUnitaria.xlsx` vía `POST /ventas-unitarias/importar-excel`, o usar el botón **Cargar y Procesar Ventas** en la vista **Data Procesada**.
5. **Procesar**: dentro del modal abierto, elegir **Procesar Todos los Ciclos** o **Procesar Periodo Específico**. Al finalizar, la página se recargará automáticamente.

Una vez completados estos pasos, el dashboard mostrará los datos procesados.

---

## 9. Solución de Problemas

### 9.1 Errores Comunes

**Error: ModuleNotFoundError**
```bash
# Solución: Asegurar entorno virtual activado
.\venv\Scripts\Activate.ps1
pip install <modulo_faltante>
```

**Error: Database locked**
```bash
# Solución: Cerrar conexiones activas o reiniciar backend
# Verificar que no haya otra instancia de uvicorn corriendo
```

**Error: JSON decode error en seed_database.py**
```bash
# Solución: Verificar formato de db.json
python -m json.tool db.json  # Validar JSON
```

**Error: CORS en frontend**
```bash
# Solución: Verificar configuración CORS en main.py
# Asegurar que el origen del frontend esté permitido
```

### 9.2 Errores en Docker

**Error: `ModuleNotFoundError: No module named 'etl'` al iniciar el backend**
```bash
# Causa: PYTHONPATH no incluye /app al ejecutar seed_database.py
# Solución: Asegúrate de usar el docker-compose.yml actualizado,
# donde el comando incluye: PYTHONPATH=/app python etl/seed_database.py
```

**Error: `permission denied` al ejecutar Docker**
```bash
# Causa: El usuario no pertenece al grupo docker
# Solución: Agregar usuario al grupo y reiniciar sesión
sudo usermod -aG docker $USER
newgrp docker
# O usar sudo temporalmente
sudo docker compose up --build
```

**Error: `404 Not Found` al procesar un periodo (`POST /data-procesada/procesar/{periodo}`)**
```bash
# Causa: No existen ventas unitarias o cierres UF para el periodo indicado.
# Solución:
# 1. Cargar ventas: POST /ventas-unitarias/importar-excel
# 2. Cargar cierres UF: POST /cierres-uf/importar-json
# 3. Volver a ejecutar el procesamiento
```

**Error: `422 Unprocessable Entity` al actualizar cierres UF desde API**
```bash
# Causa: El frontend envía { anios: [2025, 2026] } pero el backend esperaba la lista directa.
# Solución: Corregido en routers/data.py usando Body([2025, 2026], embed=True).
# Reconstruir imagen con: docker compose up --build
```

### 9.3 Verificación de Conexión a Base de Datos

```python
# En terminal Python
python
>>> from database import init_database
>>> init_database()
True  # Si la conexión es exitosa
```

### 9.4 Logs y Debugging

- **Backend logs:** Consola donde se ejecuta `uvicorn` o `docker logs evaluacion_backend`
- **Frontend logs:** Consola del navegador (F12) y terminal Vite o `docker logs evaluacion_frontend`
- **Base de datos:** Archivo `data/data_science.db` (SQLite) mapeado mediante volumen

---

## 10. Estructura del Proyecto

```
Evaluacion_3/
├── api/                    # Módulos de API auxiliares
│   ├── __init__.py
│   └── uf.py              # Integración API UF
├── dashboards/            # Frontend React
│   ├── public/            # Archivos estáticos
│   ├── src/               # Código fuente React
│   │   ├── components/    # Componentes reutilizables
│   │   ├── pages/         # Páginas de la aplicación
│   │   ├── App.jsx        # Componente principal
│   │   └── main.jsx       # Punto de entrada
│   ├── package.json       # Dependencias Node.js
│   └── vite.config.js     # Configuración Vite
├── Parametros/            # Archivos de parámetros
│   ├── cierreUF.json      # Cierres de UF
│   └── tarifas.json       # Tarifas por producto
├── routers/               # Rutas de la API
│   ├── __init__.py
│   ├── analysis.py        # Endpoints de análisis
│   ├── data.py            # Endpoints de datos
│   └── health.py          # Health check
├── config.py              # Configuración de la aplicación
├── database.py            # Conexión a base de datos
├── main.py                # Punto de entrada FastAPI
├── models.py              # Modelos SQLAlchemy
├── schemas.py             # Esquemas Pydantic
├── seed_database.py       # Script de poblado inicial
├── generate_db_json.py    # Generador de db.json desde tarifas.json
├── db.json                # Datos iniciales de productos
├── requirements.txt       # Dependencias Python
├── Dockerfile.backend     # Imagen Docker del backend
├── Dockerfile.frontend    # Imagen Docker del frontend
├── docker-compose.yml     # Orquestación de servicios
├── .dockerignore          # Archivos excluidos de las imágenes Docker
└── .env                   # Variables de entorno
```

---

## 11. Consideraciones de Seguridad

### 11.1 Para Producción

- **CORS:** Configurar orígenes permitidos específicos en `main.py`
- **Base de datos:** Usar PostgreSQL/MySQL con credenciales seguras
- **Variables de entorno:** Nunca commits de `.env` con datos sensibles
- **HTTPS:** Configurar SSL/TLS para la API
- **Autenticación:** Implementar JWT OAuth2 para endpoints protegidos

### 11.2 Archivos Sensibles

Archivos a excluir del control de versiones (ya en `.gitignore`):
```
venv/
__pycache__/
*.pyc
.env
data_science.db
node_modules/
```

---

## 12. Screenshots

### 12.1 Dashboard

![alt text](image.png)

Vista general del sistema. Muestra estadísticas de productos y ventas cargadas, gráfico comparativo de ventas por ciclo (mes/año), y gráficos de Total CLP procesado por año y por periodo. Incluye alerta automática cuando hay ventas sin procesar y acceso rápido a las secciones principales.

---

### 12.2 Productos

![alt text](image-1.png)

Catálogo de productos de reciclaje cargados en el sistema. Permite buscar por nombre, código o categoría, y gestionar (crear, editar, eliminar) cada producto con sus atributos: código ERP, código interno, peso en toneladas y gramos, categoría, material y nivel de riesgo.

---

### 12.3 Cierre UF

![alt text](image-2.png)

Tabla de valores de cierre de la UF por periodo (formato YYYYMM). Los valores son utilizados para convertir los totales calculados en UF a pesos chilenos (CLP) durante el procesamiento. Permite actualizar los valores manualmente, importar desde JSON o sincronizar automáticamente desde la API de mindicador.cl.

---

### 12.4 Data Procesada

![alt text](image-3.png)

Resultados del procesamiento de ventas. Muestra por cada periodo y producto: toneladas, gramos, cantidad, total en UF y total en CLP. Incluye gráficos de toneladas por categoría y CLP por periodo, filtros por periodo y búsqueda por categoría/material/celda. Permite cargar el Excel de ventas y ejecutar el procesamiento desde esta misma vista.

---

### 12.5 Docker

![alt text](image-4.png)


## 13. Contacto y Soporte

Para consultas técnicas o reporte de errores, contactar al equipo de desarrollo.

**Versión del Sistema:** 1.0.0
**Última Actualización:** Junio 2026