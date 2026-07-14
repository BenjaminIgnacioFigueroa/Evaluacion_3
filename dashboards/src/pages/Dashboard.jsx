import { useState, useEffect } from 'react';
import { 
  Package, 
  ShoppingCart, 
  RefreshCw,
  Filter,
  FileText,
  DollarSign,
  AlertTriangle,
  Play
} from 'lucide-react';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import {
  getProductos,
  getVentasUnitarias,
  getDataProcesada,
  procesarTodosCiclos
} from '../services/api';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

const StatCard = ({ title, value, icon: Icon, change, changeType }) => (
  <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        <p className="mt-2 text-3xl font-bold text-foreground">{value}</p>
        {change && (
          <p className={`mt-2 text-sm ${changeType === 'positive' ? 'text-green-600' : 'text-red-600'}`}>
            {change}
          </p>
        )}
      </div>
      <div className="rounded-full bg-primary/10 p-3">
        <Icon className="h-6 w-6 text-primary" />
      </div>
    </div>
  </div>
);

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    productos: 0,
    ventas: 0,
    dataProcesada: 0,
    totalClp: 0
  });
  const [procesando, setProcesando] = useState(false);
  const [processMsg, setProcessMsg] = useState('');
  const [ventasPorCiclo, setVentasPorCiclo] = useState([]);
  const [selectedCiclo, setSelectedCiclo] = useState('');
  const [availableCiclos, setAvailableCiclos] = useState([]);
  const [totalClpByYear, setTotalClpByYear] = useState([]);
  const [totalClpByMonth, setTotalClpByMonth] = useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  useEffect(() => {
    if (selectedCiclo) {
      applyFilters();
    } else {
      loadDashboardData();
    }
  }, [selectedCiclo]);

  const formatCiclo = (ciclo) => {
    const year = ciclo.substring(0, 4);
    const month = ciclo.substring(4, 6);
    const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    const monthName = meses[parseInt(month) - 1];
    return `${monthName} ${year}`;
  };

  const applyFilters = async () => {
    try {
      setLoading(true);
      
      const ventas = await getVentasUnitarias();

      // Filtrar ventas por mes seleccionado (manteniendo todos los años para ese mes)
      let filteredVentas = ventas;
      if (selectedCiclo) {
        const selectedMonth = selectedCiclo.substring(4, 6);
        filteredVentas = filteredVentas.filter(v => v.ciclo.substring(4, 6) === selectedMonth);
      }

      setStats(prev => ({
        ...prev,
        ventas: filteredVentas.length
      }));

      // Actualizar gráfico de ventas por ciclo con datos filtrados
      const ventasMonthYearData = filteredVentas.reduce((acc, venta) => {
        const year = venta.ciclo.substring(0, 4);
        const month = parseInt(venta.ciclo.substring(4, 6));
        const key = `${month}`;
        
        if (!acc[key]) {
          acc[key] = {};
        }
        acc[key][year] = (acc[key][year] || 0) + venta.cantidad;
        return acc;
      }, {});

      const ventasCicloData = Object.entries(ventasMonthYearData)
        .map(([month, years]) => ({
          mes: parseInt(month),
          ...years
        }))
        .sort((a, b) => a.mes - b.mes);
      setVentasPorCiclo(ventasCicloData);

    } catch (error) {
      console.error('Error applying filters:', error);
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setSelectedCiclo('');
    loadDashboardData();
  };

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Cargar estadísticas básicas
      const [productos, ventas, dataProc] = await Promise.all([
        getProductos(),
        getVentasUnitarias(),
        getDataProcesada()
      ]);

      const totalClp = dataProc.reduce((sum, d) => sum + (d.total_clp || 0), 0);
      setStats({
        productos: productos.length,
        ventas: ventas.length,
        dataProcesada: dataProc.length,
        totalClp
      });

      // Agrupar ventas por mes y año (para gráfico comparativo)
      const ventasMonthYearData = ventas.reduce((acc, venta) => {
        const year = venta.ciclo.substring(0, 4);
        const month = parseInt(venta.ciclo.substring(4, 6));
        const key = `${month}`;
        
        if (!acc[key]) {
          acc[key] = {};
        }
        acc[key][year] = (acc[key][year] || 0) + venta.cantidad;
        return acc;
      }, {});

      const ventasCicloData = Object.entries(ventasMonthYearData)
        .map(([month, years]) => ({
          mes: parseInt(month),
          ...years
        }))
        .sort((a, b) => a.mes - b.mes);
      setVentasPorCiclo(ventasCicloData);

      // Extraer ciclos únicos para el filtro
      const uniqueCiclos = [...new Set(ventas.map(v => v.ciclo))].sort();
      setAvailableCiclos(uniqueCiclos);

      // Procesar data procesada para gráficos
      // Agrupar total_clp por año (para pie chart)
      const totalByYear = dataProc.reduce((acc, item) => {
        const year = item.periodo.substring(0, 4);
        acc[year] = (acc[year] || 0) + (item.total_clp || 0);
        return acc;
      }, {});

      const yearData = Object.entries(totalByYear)
        .map(([year, total]) => ({ name: year, value: total }))
        .sort((a, b) => a.name.localeCompare(b.name));
      setTotalClpByYear(yearData);

      // Agrupar total_clp por mes y año (para bar chart)
      const monthYearData = dataProc.reduce((acc, item) => {
        const year = item.periodo.substring(0, 4);
        const month = parseInt(item.periodo.substring(4, 6));
        const key = `${month}`;
        
        if (!acc[key]) {
          acc[key] = {};
        }
        acc[key][year] = (acc[key][year] || 0) + (item.total_clp || 0);
        return acc;
      }, {});

      const monthChartData = Object.entries(monthYearData)
        .map(([month, years]) => ({
          mes: parseInt(month),
          ...years
        }))
        .sort((a, b) => a.mes - b.mes);
      setTotalClpByMonth(monthChartData);

    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

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
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground">
            Vista general del sistema de gestión de reciclaje
          </p>
        </div>
        <button
          onClick={loadDashboardData}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          <RefreshCw size={16} />
          Actualizar
        </button>
      </div>

      {/* Filters */}
      <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
        <div className="mb-4 flex items-center gap-2">
          <Filter className="h-5 w-5 text-primary" />
          <h3 className="text-lg font-semibold text-foreground">Filtros</h3>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className="mb-2 block text-sm font-medium text-foreground">
              Ciclo
            </label>
            <select
              value={selectedCiclo}
              onChange={(e) => setSelectedCiclo(e.target.value)}
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Todos los ciclos</option>
              {availableCiclos.map((ciclo) => (
                <option key={ciclo} value={ciclo}>
                  {formatCiclo(ciclo)}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={clearFilters}
              className="w-full rounded-md border border-input bg-background px-4 py-2 text-sm font-medium text-foreground hover:bg-accent hover:text-accent-foreground"
            >
              Limpiar Filtros
            </button>
          </div>
        </div>
      </div>

      {/* Warning banner when data_procesada is empty */}
      {stats.dataProcesada === 0 && stats.ventas > 0 && (
        <div className="flex items-center gap-3 rounded-lg border border-yellow-400 bg-yellow-50 p-4 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300">
          <AlertTriangle className="h-5 w-5 shrink-0" />
          <span className="flex-1 text-sm">
            Hay <strong>{stats.ventas}</strong> ventas cargadas pero no se han procesado. Ve a <strong>Data Procesada</strong> y haz clic en "Cargar y Procesar Ventas" → "Procesar Todos los Ciclos".
          </span>
          <button
            onClick={async () => {
              setProcesando(true);
              setProcessMsg('');
              try {
                const result = await procesarTodosCiclos();
                setProcessMsg(`Procesados: ${result.ciclos_procesados} ciclos. ${(result.errores || []).join(' | ')}`);
                await loadDashboardData();
              } catch (e) {
                setProcessMsg('Error: ' + e.message);
              } finally {
                setProcesando(false);
              }
            }}
            disabled={procesando}
            className="flex shrink-0 items-center gap-1 rounded-md bg-yellow-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-yellow-700 disabled:opacity-50"
          >
            <Play size={12} />
            {procesando ? 'Procesando...' : 'Procesar ahora'}
          </button>
        </div>
      )}
      {processMsg && (
        <div className="rounded-lg border border-border bg-card p-3 text-sm text-muted-foreground">
          {processMsg}
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-2">
        <StatCard
          title="Productos"
          value={stats.productos}
          icon={Package}
        />
        <StatCard
          title="Ventas Unitarias"
          value={stats.ventas}
          icon={ShoppingCart}
        />
      </div>

      {/* Data Procesada summary */}
      {stats.dataProcesada > 0 && (
        <div className="grid gap-4 md:grid-cols-2">
          <StatCard
            title="Registros Procesados"
            value={stats.dataProcesada.toLocaleString('es-CL')}
            icon={FileText}
          />
          <StatCard
            title="Total CLP Procesado"
            value={`$ ${stats.totalClp.toLocaleString('es-CL')}`}
            icon={DollarSign}
          />
        </div>
      )}

      {/* Charts */}
      <div className="grid gap-6 md:grid-cols-1">
        {/* Ventas por Ciclo */}
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-foreground">Ventas por Ciclo (Cantidad por mes y año)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={ventasPorCiclo} barSize={20}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="mes" />
              <YAxis />
              <Tooltip />
              <Legend />
              {Object.keys(ventasPorCiclo.length > 0 ? ventasPorCiclo[0] : {}).filter(key => key !== 'mes').map((year, index) => (
                <Bar 
                  key={year} 
                  dataKey={year} 
                  fill={COLORS[index % COLORS.length]} 
                  name={year}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Data Procesada Charts */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Pie Chart - Total CLP por Año */}
          <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
            <h3 className="mb-4 text-lg font-semibold text-foreground">Total CLP por Año</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={totalClpByYear}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(2)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {totalClpByYear.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `${(value / 1000000).toFixed(2)} mill.`} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Bar Chart - Total CLP por Mes y Año */}
          <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
            <h3 className="mb-4 text-lg font-semibold text-foreground">Suma de total_clp por mes y año</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={totalClpByMonth} barSize={20}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="mes" />
                <YAxis tickFormatter={(value) => `${(value / 1000000).toFixed(1)} mil.`} />
                <Tooltip formatter={(value) => `${(value / 1000000).toFixed(2)} mill.`} />
                <Legend />
                {Object.keys(totalClpByMonth.length > 0 ? totalClpByMonth[0] : {}).filter(key => key !== 'mes').map((year, index) => (
                  <Bar 
                    key={year} 
                    dataKey={year} 
                    fill={COLORS[index % COLORS.length]} 
                    name={year}
                  />
                ))}
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
        <h3 className="mb-4 text-lg font-semibold text-foreground">Acciones Rápidas</h3>
        <div className="grid gap-4 md:grid-cols-3">
          <a
            href="/productos"
            className="flex items-center gap-3 rounded-lg border border-border p-4 hover:bg-accent hover:text-accent-foreground"
          >
            <Package className="h-5 w-5" />
            <div>
              <p className="font-medium">Gestionar Productos</p>
              <p className="text-sm text-muted-foreground">Crear, editar y eliminar productos</p>
            </div>
          </a>
          <a
            href="/ventas"
            className="flex items-center gap-3 rounded-lg border border-border p-4 hover:bg-accent hover:text-accent-foreground"
          >
            <ShoppingCart className="h-5 w-5" />
            <div>
              <p className="font-medium">Gestionar Ventas</p>
              <p className="text-sm text-muted-foreground">Registrar y consultar ventas</p>
            </div>
          </a>
          <a
            href="/data-procesada"
            className="flex items-center gap-3 rounded-lg border border-border p-4 hover:bg-accent hover:text-accent-foreground"
          >
            <FileText className="h-5 w-5" />
            <div>
              <p className="font-medium">Ver Data Procesada</p>
              <p className="text-sm text-muted-foreground">Análisis de datos procesados</p>
            </div>
          </a>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
