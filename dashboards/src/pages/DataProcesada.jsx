import { useState, useEffect } from 'react';
import { Search, RefreshCw, Play, TrendingUp, DollarSign, Package } from 'lucide-react';
import {
  getDataProcesada,
  getDataProcesadaByPeriodo,
  procesarDatos
} from '../services/api';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const DataProcesada = () => {
  const [dataProcesada, setDataProcesada] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterPeriodo, setFilterPeriodo] = useState('');
  const [showProcessModal, setShowProcessModal] = useState(false);
  const [periodoToProcess, setPeriodoToProcess] = useState('');
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    loadDataProcesada();
  }, []);

  const loadDataProcesada = async () => {
    try {
      setLoading(true);
      const data = await getDataProcesada();
      setDataProcesada(data);
    } catch (error) {
      console.error('Error loading data procesada:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProcess = async (e) => {
    e.preventDefault();
    if (!periodoToProcess) {
      alert('Por favor ingrese un periodo');
      return;
    }
    try {
      setProcessing(true);
      await procesarDatos(periodoToProcess);
      alert('Procesamiento completado exitosamente');
      setShowProcessModal(false);
      setPeriodoToProcess('');
      loadDataProcesada();
    } catch (error) {
      console.error('Error processing data:', error);
      alert('Error al procesar datos: ' + error.message);
    } finally {
      setProcessing(false);
    }
  };

  const periodosUnicos = [...new Set(dataProcesada.map(d => d.periodo))].sort();

  const filteredData = dataProcesada.filter(d => {
    const matchesSearch = 
      d.categoria.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.material.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.celda.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPeriodo = !filterPeriodo || d.periodo === filterPeriodo;
    return matchesSearch && matchesPeriodo;
  });

  // Datos para gráficos
  const dataByCategoria = filteredData.reduce((acc, item) => {
    acc[item.categoria] = (acc[item.categoria] || 0) + item.total_tonelada;
    return acc;
  }, {});

  const categoriaChartData = Object.entries(dataByCategoria)
    .map(([categoria, total]) => ({ categoria, total }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 10);

  const dataByPeriodo = filteredData.reduce((acc, item) => {
    acc[item.periodo] = (acc[item.periodo] || 0) + item.total_clp;
    return acc;
  }, {});

  const periodoChartData = Object.entries(dataByPeriodo)
    .map(([periodo, total]) => ({ periodo, total }))
    .sort((a, b) => a.periodo.localeCompare(b.periodo));

  // Totales
  const totalToneladas = filteredData.reduce((sum, item) => sum + item.total_tonelada, 0);
  const totalUF = filteredData.reduce((sum, item) => sum + item.total_uf, 0);
  const totalCLP = filteredData.reduce((sum, item) => sum + item.total_clp, 0);

  if (loading) {
    return (
      <div className="flex items-center justify-center">
        <RefreshCw className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Data Procesada</h1>
          <p className="text-muted-foreground">Análisis de datos procesados con cálculos de UF y CLP</p>
        </div>
        <button
          onClick={() => setShowProcessModal(true)}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          <Play size={16} />
          Procesar Periodo
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">Total Toneladas</p>
              <p className="mt-2 text-3xl font-bold text-foreground">{totalToneladas.toFixed(5)}</p>
            </div>
            <div className="rounded-full bg-primary/10 p-3">
              <Package className="h-6 w-6 text-primary" />
            </div>
          </div>
        </div>
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">Total UF</p>
              <p className="mt-2 text-3xl font-bold text-foreground">{totalUF.toFixed(2)}</p>
            </div>
            <div className="rounded-full bg-primary/10 p-3">
              <TrendingUp className="h-6 w-6 text-primary" />
            </div>
          </div>
        </div>
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">Total CLP</p>
              <p className="mt-2 text-3xl font-bold text-foreground">$ {totalCLP.toLocaleString('es-CL')}</p>
            </div>
            <div className="rounded-full bg-primary/10 p-3">
              <DollarSign className="h-6 w-6 text-primary" />
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Buscar por categoría, material o celda..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full rounded-lg border border-border bg-background pl-10 pr-4 py-2 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
        <select
          value={filterPeriodo}
          onChange={(e) => setFilterPeriodo(e.target.value)}
          className="rounded-lg border border-border bg-background px-4 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option value="">Todos los periodos</option>
          {periodosUnicos.map(periodo => (
            <option key={periodo} value={periodo}>{periodo}</option>
          ))}
        </select>
      </div>

      {/* Charts */}
      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-foreground">Toneladas por Categoría</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categoriaChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="categoria" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="total" fill="#3b82f6" name="Toneladas" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-foreground">Total CLP por Periodo</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={periodoChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="periodo" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="total" 
                stroke="#10b981" 
                strokeWidth={2}
                name="Total CLP"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Table */}
      <div className="rounded-lg border border-border bg-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Periodo</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Código</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Celda</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Categoría</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Material</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Riesgo</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-muted-foreground">Toneladas</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-muted-foreground">Gramos</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-muted-foreground">Cantidad</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-muted-foreground">Total UF</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-muted-foreground">Total CLP</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.map((item) => (
                <tr key={item.id} className="border-t border-border hover:bg-accent/50">
                  <td className="px-4 py-3 text-sm text-foreground">{item.periodo}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{item.codigo_interno}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{item.celda}</td>
                  <td className="px-4 py-3 text-sm font-medium text-foreground">{item.categoria}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{item.material}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{item.riesgo}</td>
                  <td className="px-4 py-3 text-right text-sm text-foreground">{item.total_tonelada.toFixed(5)}</td>
                  <td className="px-4 py-3 text-right text-sm text-foreground">{item.total_gramos.toFixed(5)}</td>
                  <td className="px-4 py-3 text-right text-sm text-foreground">{item.cantidad_total}</td>
                  <td className="px-4 py-3 text-right text-sm text-foreground">{item.total_uf.toFixed(2)}</td>
                  <td className="px-4 py-3 text-right text-sm text-foreground">$ {item.total_clp.toLocaleString('es-CL')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {filteredData.length === 0 && (
          <div className="p-8 text-center text-muted-foreground">
            No se encontraron datos procesados
          </div>
        )}
      </div>

      {/* Modal Procesar */}
      {showProcessModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-md rounded-lg bg-card p-6 shadow-lg">
            <h2 className="mb-4 text-xl font-bold text-foreground">Procesar Datos por Periodo</h2>
            <form onSubmit={handleProcess} className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">Periodo (YYYYMM)</label>
                <input
                  type="text"
                  required
                  placeholder="Ej: 202501"
                  value={periodoToProcess}
                  onChange={(e) => setPeriodoToProcess(e.target.value)}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
                <p className="mt-2 text-xs text-muted-foreground">
                  Esto procesará las ventas del periodo y generará los cálculos de UF y CLP
                </p>
              </div>
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowProcessModal(false);
                    setPeriodoToProcess('');
                  }}
                  className="rounded-lg border border-border px-4 py-2 text-sm font-medium text-foreground hover:bg-accent"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={processing}
                  className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
                >
                  {processing ? 'Procesando...' : 'Procesar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataProcesada;
