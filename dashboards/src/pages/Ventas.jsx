import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Search, RefreshCw, Upload, FileSpreadsheet } from 'lucide-react';
import {
  getVentasUnitarias,
  createVentaUnitaria,
  updateVentaUnitaria,
  deleteVentaUnitaria,
  importarVentasExcel,
  getVentasByCiclo
} from '../services/api';

const Ventas = () => {
  const [ventas, setVentas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCiclo, setFilterCiclo] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [editingVenta, setEditingVenta] = useState(null);
  const [formData, setFormData] = useState({
    ciclo: '',
    codigo_erp: '',
    cantidad: ''
  });
  const [importFile, setImportFile] = useState(null);
  const [importing, setImporting] = useState(false);

  useEffect(() => {
    loadVentas();
  }, []);

  const loadVentas = async () => {
    try {
      setLoading(true);
      const data = await getVentasUnitarias();
      setVentas(data);
    } catch (error) {
      console.error('Error loading ventas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        cantidad: parseFloat(formData.cantidad)
      };

      if (editingVenta) {
        await updateVentaUnitaria(editingVenta.id, payload);
      } else {
        await createVentaUnitaria(payload);
      }
      
      setShowModal(false);
      setEditingVenta(null);
      resetForm();
      loadVentas();
    } catch (error) {
      console.error('Error saving venta:', error);
      alert('Error al guardar venta');
    }
  };

  const handleImport = async (e) => {
    e.preventDefault();
    if (!importFile) {
      alert('Por favor seleccione un archivo Excel');
      return;
    }
    try {
      setImporting(true);
      await importarVentasExcel(importFile);
      alert('Importación completada exitosamente');
      setShowImportModal(false);
      setImportFile(null);
      loadVentas();
    } catch (error) {
      console.error('Error importing ventas:', error);
      alert('Error al importar ventas: ' + error.message);
    } finally {
      setImporting(false);
    }
  };

  const handleEdit = (venta) => {
    setEditingVenta(venta);
    setFormData({
      ciclo: venta.ciclo,
      codigo_erp: venta.codigo_erp,
      cantidad: venta.cantidad
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar esta venta?')) {
      try {
        await deleteVentaUnitaria(id);
        loadVentas();
      } catch (error) {
        console.error('Error deleting venta:', error);
        alert('Error al eliminar venta');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      ciclo: '',
      codigo_erp: '',
      cantidad: ''
    });
  };

  const filteredVentas = ventas.filter(v => {
    const matchesSearch = v.codigo_erp.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCiclo = !filterCiclo || v.ciclo === filterCiclo;
    return matchesSearch && matchesCiclo;
  });

  const ciclosUnicos = [...new Set(ventas.map(v => v.ciclo))].sort();

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
          <h1 className="text-3xl font-bold text-foreground">Ventas Unitarias</h1>
          <p className="text-muted-foreground">Gestión de ventas mensuales por producto</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowImportModal(true)}
            className="flex items-center gap-2 rounded-lg border border-border px-4 py-2 text-sm font-medium text-foreground hover:bg-accent"
          >
            <Upload size={16} />
            Importar Excel
          </button>
          <button
            onClick={() => {
              resetForm();
              setEditingVenta(null);
              setShowModal(true);
            }}
            className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
          >
            <Plus size={16} />
            Nueva Venta
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Buscar por código ERP..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full rounded-lg border border-border bg-background pl-10 pr-4 py-2 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
        <select
          value={filterCiclo}
          onChange={(e) => setFilterCiclo(e.target.value)}
          className="rounded-lg border border-border bg-background px-4 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option value="">Todos los ciclos</option>
          {ciclosUnicos.map(ciclo => (
            <option key={ciclo} value={ciclo}>{ciclo}</option>
          ))}
        </select>
      </div>

      {/* Table */}
      <div className="rounded-lg border border-border bg-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Ciclo</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Código ERP</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Cantidad</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-muted-foreground">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filteredVentas.map((venta) => (
                <tr key={venta.id} className="border-t border-border hover:bg-accent/50">
                  <td className="px-4 py-3 text-sm text-foreground">{venta.ciclo}</td>
                  <td className="px-4 py-3 text-sm font-medium text-foreground">{venta.codigo_erp}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{venta.cantidad}</td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => handleEdit(venta)}
                        className="rounded p-1 hover:bg-accent hover:text-accent-foreground"
                      >
                        <Edit size={16} />
                      </button>
                      <button
                        onClick={() => handleDelete(venta.id)}
                        className="rounded p-1 hover:bg-destructive hover:text-destructive-foreground"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {filteredVentas.length === 0 && (
          <div className="p-8 text-center text-muted-foreground">
            No se encontraron ventas
          </div>
        )}
      </div>

      {/* Modal Crear/Editar */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-md rounded-lg bg-card p-6 shadow-lg">
            <h2 className="mb-4 text-xl font-bold text-foreground">
              {editingVenta ? 'Editar Venta' : 'Nueva Venta'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">Ciclo (YYYYMM)</label>
                <input
                  type="text"
                  required
                  placeholder="Ej: 202501"
                  value={formData.ciclo}
                  onChange={(e) => setFormData({ ...formData, ciclo: e.target.value })}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">Código ERP</label>
                <input
                  type="text"
                  required
                  value={formData.codigo_erp}
                  onChange={(e) => setFormData({ ...formData, codigo_erp: e.target.value })}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">Cantidad</label>
                <input
                  type="number"
                  step="0.01"
                  required
                  value={formData.cantidad}
                  onChange={(e) => setFormData({ ...formData, cantidad: e.target.value })}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingVenta(null);
                    resetForm();
                  }}
                  className="rounded-lg border border-border px-4 py-2 text-sm font-medium text-foreground hover:bg-accent"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
                >
                  {editingVenta ? 'Actualizar' : 'Crear'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Importar */}
      {showImportModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-md rounded-lg bg-card p-6 shadow-lg">
            <h2 className="mb-4 text-xl font-bold text-foreground">Importar Ventas desde Excel</h2>
            <form onSubmit={handleImport} className="space-y-4">
              <div className="flex items-center justify-center rounded-lg border-2 border-dashed border-border p-8">
                <div className="text-center">
                  <FileSpreadsheet className="mx-auto h-12 w-12 text-muted-foreground" />
                  <p className="mt-2 text-sm text-muted-foreground">
                    {importFile ? importFile.name : 'Seleccione un archivo Excel (.xlsx, .xls)'}
                  </p>
                  <input
                    type="file"
                    accept=".xlsx,.xls"
                    onChange={(e) => setImportFile(e.target.files[0])}
                    className="mt-2"
                  />
                </div>
              </div>
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowImportModal(false);
                    setImportFile(null);
                  }}
                  className="rounded-lg border border-border px-4 py-2 text-sm font-medium text-foreground hover:bg-accent"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={importing}
                  className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
                >
                  {importing ? 'Importando...' : 'Importar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Ventas;
