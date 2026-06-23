import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Search, RefreshCw, Upload, FileJson } from 'lucide-react';
import {
  getTarifas,
  createTarifa,
  updateTarifa,
  deleteTarifa,
  importarTarifasJson
} from '../services/api';

const Tarifas = () => {
  const [tarifas, setTarifas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [editingTarifa, setEditingTarifa] = useState(null);
  const [formData, setFormData] = useState({
    codigo: '',
    celda: '',
    t2025: '',
    t2026: ''
  });
  const [importFile, setImportFile] = useState(null);
  const [importing, setImporting] = useState(false);

  useEffect(() => {
    loadTarifas();
  }, []);

  const loadTarifas = async () => {
    try {
      setLoading(true);
      const data = await getTarifas();
      setTarifas(data);
    } catch (error) {
      console.error('Error loading tarifas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        codigo: parseInt(formData.codigo),
        t2025: parseFloat(formData.t2025),
        t2026: parseFloat(formData.t2026)
      };

      if (editingTarifa) {
        await updateTarifa(editingTarifa.id, payload);
      } else {
        await createTarifa(payload);
      }
      
      setShowModal(false);
      setEditingTarifa(null);
      resetForm();
      loadTarifas();
    } catch (error) {
      console.error('Error saving tarifa:', error);
      alert('Error al guardar tarifa');
    }
  };

  const handleImport = async (e) => {
    e.preventDefault();
    if (!importFile) {
      alert('Por favor seleccione un archivo JSON');
      return;
    }
    try {
      setImporting(true);
      await importarTarifasJson(importFile);
      alert('Importación completada exitosamente');
      setShowImportModal(false);
      setImportFile(null);
      loadTarifas();
    } catch (error) {
      console.error('Error importing tarifas:', error);
      alert('Error al importar tarifas: ' + error.message);
    } finally {
      setImporting(false);
    }
  };

  const handleEdit = (tarifa) => {
    setEditingTarifa(tarifa);
    setFormData({
      codigo: tarifa.codigo,
      celda: tarifa.celda,
      t2025: tarifa.t2025,
      t2026: tarifa.t2026
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar esta tarifa?')) {
      try {
        await deleteTarifa(id);
        loadTarifas();
      } catch (error) {
        console.error('Error deleting tarifa:', error);
        alert('Error al eliminar tarifa');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      codigo: '',
      celda: '',
      t2025: '',
      t2026: ''
    });
  };

  const filteredTarifas = tarifas.filter(t =>
    t.celda.toLowerCase().includes(searchTerm.toLowerCase()) ||
    t.codigo.toString().includes(searchTerm)
  );

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
          <h1 className="text-3xl font-bold text-foreground">Tarifas</h1>
          <p className="text-muted-foreground">Gestión de tarifas por producto (UF/tonelada)</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowImportModal(true)}
            className="flex items-center gap-2 rounded-lg border border-border px-4 py-2 text-sm font-medium text-foreground hover:bg-accent"
          >
            <Upload size={16} />
            Importar JSON
          </button>
          <button
            onClick={() => {
              resetForm();
              setEditingTarifa(null);
              setShowModal(true);
            }}
            className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
          >
            <Plus size={16} />
            Nueva Tarifa
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input
          type="text"
          placeholder="Buscar por código o celda..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full rounded-lg border border-border bg-background pl-10 pr-4 py-2 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        />
      </div>

      {/* Table */}
      <div className="rounded-lg border border-border bg-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Código</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Celda</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Tarifa 2025 (UF/ton)</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Tarifa 2026 (UF/ton)</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-muted-foreground">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filteredTarifas.map((tarifa) => (
                <tr key={tarifa.id} className="border-t border-border hover:bg-accent/50">
                  <td className="px-4 py-3 text-sm text-foreground">{tarifa.codigo}</td>
                  <td className="px-4 py-3 text-sm font-medium text-foreground">{tarifa.celda}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{tarifa.t2025}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{tarifa.t2026}</td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => handleEdit(tarifa)}
                        className="rounded p-1 hover:bg-accent hover:text-accent-foreground"
                      >
                        <Edit size={16} />
                      </button>
                      <button
                        onClick={() => handleDelete(tarifa.id)}
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
        {filteredTarifas.length === 0 && (
          <div className="p-8 text-center text-muted-foreground">
            No se encontraron tarifas
          </div>
        )}
      </div>

      {/* Modal Crear/Editar */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-md rounded-lg bg-card p-6 shadow-lg">
            <h2 className="mb-4 text-xl font-bold text-foreground">
              {editingTarifa ? 'Editar Tarifa' : 'Nueva Tarifa'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">Código</label>
                <input
                  type="number"
                  required
                  value={formData.codigo}
                  onChange={(e) => setFormData({ ...formData, codigo: e.target.value })}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">Celda</label>
                <input
                  type="text"
                  required
                  value={formData.celda}
                  onChange={(e) => setFormData({ ...formData, celda: e.target.value })}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">Tarifa 2025 (UF/ton)</label>
                <input
                  type="number"
                  step="0.01"
                  required
                  value={formData.t2025}
                  onChange={(e) => setFormData({ ...formData, t2025: e.target.value })}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">Tarifa 2026 (UF/ton)</label>
                <input
                  type="number"
                  step="0.01"
                  required
                  value={formData.t2026}
                  onChange={(e) => setFormData({ ...formData, t2026: e.target.value })}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingTarifa(null);
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
                  {editingTarifa ? 'Actualizar' : 'Crear'}
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
            <h2 className="mb-4 text-xl font-bold text-foreground">Importar Tarifas desde JSON</h2>
            <form onSubmit={handleImport} className="space-y-4">
              <div className="flex items-center justify-center rounded-lg border-2 border-dashed border-border p-8">
                <div className="text-center">
                  <FileJson className="mx-auto h-12 w-12 text-muted-foreground" />
                  <p className="mt-2 text-sm text-muted-foreground">
                    {importFile ? importFile.name : 'Seleccione un archivo JSON'}
                  </p>
                  <input
                    type="file"
                    accept=".json"
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

export default Tarifas;
