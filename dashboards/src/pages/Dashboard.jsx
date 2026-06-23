import { useState, useEffect } from 'react';
import { 
  Package, 
  ShoppingCart, 
  DollarSign, 
  TrendingUp, 
  FileText,
  RefreshCw
} from 'lucide-react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
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
  getTarifas,
  getCierresUF,
  getDataProcesada,
  healthCheck
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
    tarifas: 0,
    cierresUF: 0,
    dataProcesada: 0
  });
  const [ventasPorCiclo, setVentasPorCiclo] = useState([]);
  const [ventasPorCategoria, setVentasPorCategoria] = useState([]);
  const [cierresUFTrend, setCierresUFTrend] = useState([]);
  const [healthStatus, setHealthStatus] = useState('unknown');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Health check
      const health = await healthCheck();
      setHealthStatus(health.status);

      // Cargar estadísticas básicas
      const [productos, ventas, tarifas, cierres, dataProc] = await Promise.all([
        getProductos(),
        getVentasUnitarias(),
        getTarifas(),
        getCierresUF(),
        getDataProcesada()
      ]);

      setStats({
        productos: productos.length,
        ventas: ventas.length,
        tarifas: tarifas.length,
        cierresUF: cierres.length,
        dataProcesada: dataProc.length
      });

      // Agrupar ventas por ciclo
      const ventasByCiclo = ventas.reduce((acc, venta) => {
        acc[venta.ciclo] = (acc[venta.ciclo] || 0) + venta.cantidad;
        return acc;
      }, {});

      const ventasCicloData = Object.entries(ventasByCiclo)
        .map(([ciclo, cantidad]) => ({ ciclo, cantidad }))
        .sort((a, b) => a.ciclo.localeCompare(b.ciclo));
      setVentasPorCiclo(ventasCicloData);

      // Agrupar ventas por categoría (usando data procesada)
      const dataByCategoria = dataProc.reduce((acc, item) => {
        acc[item.categoria] = (acc[item.categoria] || 0) + item.total_tonelada;
        return acc;
      }, {});

      const categoriaData = Object.entries(dataByCategoria)
        .map(([categoria, total]) => ({ name: categoria, value: total }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 6);
      setVentasPorCategoria(categoriaData);

      // Tendencia de cierres UF
      const cierresTrend = cierres
        .sort((a, b) => a.ciclo.localeCompare(b.ciclo))
        .map(cierre => ({
          ciclo: cierre.ciclo,
          valor: cierre.uf_pesos
        }));
      setCierresUFTrend(cierresTrend);

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

      {/* Health Status */}
      <div className={`rounded-lg border p-4 ${
        healthStatus === 'healthy' ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'
      }`}>
        <p className={`font-medium ${
          healthStatus === 'healthy' ? 'text-green-700' : 'text-red-700'
        }`}>
          Estado del Sistema: {healthStatus === 'healthy' ? '✓ Saludable' : '✗ Error'}
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
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
        <StatCard
          title="Tarifas"
          value={stats.tarifas}
          icon={DollarSign}
        />
        <StatCard
          title="Cierres UF"
          value={stats.cierresUF}
          icon={TrendingUp}
        />
        <StatCard
          title="Data Procesada"
          value={stats.dataProcesada}
          icon={FileText}
        />
      </div>

      {/* Charts */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Ventas por Ciclo */}
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-foreground">Ventas por Ciclo</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={ventasPorCiclo}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ciclo" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="cantidad" fill="#3b82f6" name="Cantidad" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Ventas por Categoría */}
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-foreground">Ventas por Categoría (Toneladas)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={ventasPorCategoria}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {ventasPorCategoria.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Tendencia Cierres UF */}
        <div className="col-span-2 rounded-lg border border-border bg-card p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-foreground">Tendencia de Cierres UF</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={cierresUFTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ciclo" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="valor" 
                stroke="#10b981" 
                strokeWidth={2}
                name="Valor UF (CLP)"
              />
            </LineChart>
          </ResponsiveContainer>
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
