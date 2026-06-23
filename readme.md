Logica de tablas:

Data 1: VentaUnitaria.xlsx

Este archivo lo envia el área comercial, correspondiente a la facturación mensual entre 2025-01 hasta 2026-04.
Contiene las columnas:

- ciclo: mes y año en el cual se efectuo la venta.
- codigo_erp: codigo del producto vendido (se enlaza con productos_erp para saber su información y ádemas su codigo_interno)
- cantidad: total vendido por ese producto en el mes y año correspondiente.

Data 2: productos_erp (BD)

Viene de una base de datos creada en MySQL con las columnas: 

- codigo_erp
- nombre
- peso_ton
- peso_gr
- codigo_interno
- categoria
- subcategoria
- tipo_material
- material
- riesgo

nota: Esta tabla sirve para unir ventaUnitaria.codigo_erp = productos.codigo_erp, con esta union puedo identificar el codigo interno que sera usado con tarifas.json

Data 3: tarifas.json

Esta data en formato json contiene las columnas:

- codigo: Este es el codigo usado para hacer union con productos.codigo_interno = tarifas.codigo
- celda: Identifica la celda en la cual se debe almacenar el dato final en formato.xslx
- t2025: Es el valor de la tarifa en UF por cada tonelada correspondiente al año de pago 2025.
- t2026: Es el valor de la tarifa en UF por cada tonelada correspondiente al año de pago 2026.

Data 4: cierreUF.json (API)

Esta data se construye gracias al consumo de una api llamada miindicador.cl y en el caso de que no funcione se debe ingresar manualmente en el arhcivo cierreUF.json obteniendo el valor de SII

Data 5: procesada (BD)

Esta data lo que hace es contener el resultado de la lógica, es importante que me guarde las columnas:
- codigo_interno: Es el codigo usado en tarifas.json y productos.codigo_interno.
- celda: es la celda obtenida de tarifas.celda.  
- categoria: Se obtiene de productos.categoria
- subcategoria: Se obtiene de productos.subcategoria
- tipo_material: Se obtiene de productos.tipo_material
- material: se obtiene de productos.material
- riesgo: se obtiene de productos.riesgo
- total_tonelada: se obtiene de la multiplicación entre ventasUnitarias.cantidad y productos.peso_ton de cada fila para finalmente dejar la suma total de todos esos resultados según codigo interno. 
- total_gramos: se obtiene de la multiplicación entre ventasUnitarias.cantidad y productos.peso_gr de cada fila para finalmente dejar la suma total de todos esos resultados según codigo interno. 
- cantidad_total: Es la cantidad de productos vendidos según codigo interno
- total_UF: Es la suma total en UF de todos los productos vendidos
- total_clp: Es la suma total en UF multiplicada por el valor de cierreUF.json según periodo
- periodo: corresponde al periodo en el cual dejamos totalizada la venta.