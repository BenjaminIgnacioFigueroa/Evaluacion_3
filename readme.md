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

## 5. Poblado de la Base de Datos

### 5.1 Verificar Archivo de Datos

Asegúrese de que el archivo `db.json` exista en el directorio raíz con la estructura de productos.

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
uvicorn main:app --reload --host 0.0.0.0 --port 8000
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
   - Reemplazar `VentaUnitaria.xlsx`
   - Usar endpoint `POST /api/ventas` para cargar

2. **Actualizar tarifas:**
   - Modificar `Parametros/tarifas.json`
   - Usar endpoint `POST /api/tarifas` para recargar

3. **Actualizar cierres UF:**
   - Modificar `Parametros/cierreUF.json`
   - Usar endpoint `POST /api/cierres-uf` para recargar

4. **Reprocesar datos:**
   - Ejecutar `POST /api/analysis/process`

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

### 9.2 Verificación de Conexión a Base de Datos

```python
# En terminal Python
python
>>> from database import init_database
>>> init_database()
True  # Si la conexión es exitosa
```

### 9.3 Logs y Debugging

- **Backend logs:** Consola donde se ejecuta `uvicorn`
- **Frontend logs:** Consola del navegador (F12) y terminal Vite
- **Base de datos:** Archivo `data_science.db` (SQLite)

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
├── db.json                # Datos iniciales de productos
├── requirements.txt       # Dependencias Python
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

## 12. Contacto y Soporte

Para consultas técnicas o reporte de errores, contactar al equipo de desarrollo.

**Versión del Sistema:** 1.0.0
**Última Actualización:** Junio 2026