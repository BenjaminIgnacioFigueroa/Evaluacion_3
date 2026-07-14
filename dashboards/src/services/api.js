import axios from 'axios';

// Cambiar a localhost para desarrollo, ngrok para producción
const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health Check
export const healthCheck = async () => {
  const response = await api.get('/health/');
  return response.data;
};

// Productos
export const getProductos = async () => {
  const response = await api.get('/productos/');
  return response.data;
};

export const getProducto = async (id) => {
  const response = await api.get(`/productos/${id}`);
  return response.data;
};

export const getProductoByCodigo = async (codigo) => {
  const response = await api.get(`/productos/codigo/${codigo}`);
  return response.data;
};

export const createProducto = async (producto) => {
  const response = await api.post('/productos/', producto);
  return response.data;
};

export const updateProducto = async (id, producto) => {
  const response = await api.put(`/productos/${id}`, producto);
  return response.data;
};

export const deleteProducto = async (id) => {
  const response = await api.delete(`/productos/${id}`);
  return response.data;
};

// Ventas Unitarias
export const getVentasUnitarias = async () => {
  const response = await api.get('/ventas-unitarias/');
  return response.data;
};

export const getVentaUnitaria = async (id) => {
  const response = await api.get(`/ventas-unitarias/${id}`);
  return response.data;
};

export const getVentasByCiclo = async (ciclo) => {
  const response = await api.get(`/ventas-unitarias/ciclo/${ciclo}`);
  return response.data;
};

export const getVentasByProducto = async (codigoErp) => {
  const response = await api.get(`/ventas-unitarias/producto/${codigoErp}`);
  return response.data;
};

export const createVentaUnitaria = async (venta) => {
  const response = await api.post('/ventas-unitarias/', venta);
  return response.data;
};

export const updateVentaUnitaria = async (id, venta) => {
  const response = await api.put(`/ventas-unitarias/${id}`, venta);
  return response.data;
};

export const deleteVentaUnitaria = async (id) => {
  const response = await api.delete(`/ventas-unitarias/${id}`);
  return response.data;
};

export const importarVentasExcel = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/ventas-unitarias/importar-excel', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getVentasConProducto = async (ciclo) => {
  const response = await api.get(`/ventas-unitarias/join-producto/${ciclo}`);
  return response.data;
};

export const getVentasCompletas = async (ciclo) => {
  const response = await api.get(`/ventas-unitarias/join-completo/${ciclo}`);
  return response.data;
};

// Tarifas
export const getTarifas = async () => {
  const response = await api.get('/tarifas/');
  return response.data;
};

export const getTarifa = async (id) => {
  const response = await api.get(`/tarifas/${id}`);
  return response.data;
};

export const getTarifaByCodigo = async (codigo) => {
  const response = await api.get(`/tarifas/codigo/${codigo}`);
  return response.data;
};

export const createTarifa = async (tarifa) => {
  const response = await api.post('/tarifas/', tarifa);
  return response.data;
};

export const updateTarifa = async (id, tarifa) => {
  const response = await api.put(`/tarifas/${id}`, tarifa);
  return response.data;
};

export const deleteTarifa = async (id) => {
  const response = await api.delete(`/tarifas/${id}`);
  return response.data;
};

export const importarTarifasJson = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/tarifas/importar-json', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Cierres UF
export const getCierresUF = async () => {
  const response = await api.get('/cierres-uf/');
  return response.data;
};

export const getCierreUF = async (id) => {
  const response = await api.get(`/cierres-uf/${id}`);
  return response.data;
};

export const getCierreUFByCiclo = async (ciclo) => {
  const response = await api.get(`/cierres-uf/ciclo/${ciclo}`);
  return response.data;
};

export const createCierreUF = async (cierre) => {
  const response = await api.post('/cierres-uf/', cierre);
  return response.data;
};

export const updateCierreUF = async (id, cierre) => {
  const response = await api.put(`/cierres-uf/${id}`, cierre);
  return response.data;
};

export const deleteCierreUF = async (id) => {
  const response = await api.delete(`/cierres-uf/${id}`);
  return response.data;
};

export const importarCierresUFJson = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/cierres-uf/importar-json', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const actualizarCierresDesdeAPI = async (anios = [2025, 2026]) => {
  const response = await api.post('/cierres-uf/actualizar-desde-api', { anios });
  return response.data;
};

// Data Procesada
export const getDataProcesada = async () => {
  const response = await api.get('/data-procesada/');
  return response.data;
};

export const getDataProcesadaByPeriodo = async (periodo) => {
  const response = await api.get(`/data-procesada/periodo/${periodo}`);
  return response.data;
};

export const getDataProcesadaByCodigo = async (codigoInterno) => {
  const response = await api.get(`/data-procesada/codigo/${codigoInterno}`);
  return response.data;
};

export const createDataProcesada = async (data) => {
  const response = await api.post('/data-procesada/', data);
  return response.data;
};

export const updateDataProcesada = async (id, data) => {
  const response = await api.put(`/data-procesada/${id}`, data);
  return response.data;
};

export const deleteDataProcesada = async (id) => {
  const response = await api.delete(`/data-procesada/${id}`);
  return response.data;
};

export const procesarDatos = async (periodo) => {
  const response = await api.post(`/data-procesada/procesar/${periodo}`);
  return response.data;
};

export const procesarTodosCiclos = async () => {
  const response = await api.post('/data-procesada/procesar-todos');
  return response.data;
};

// Análisis
export const getAnalisisBasico = async () => {
  const response = await api.get('/analisis/basico');
  return response.data;
};

export default api;
