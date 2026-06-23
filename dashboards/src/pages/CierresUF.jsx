import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Search, RefreshCw, Upload, FileJson, CloudDownload } from 'lucide-react';
import {
  getCierresUF,
  createCierreUF,
  updateCierreUF,
  deleteCierreUF,
  importarCierresUFJson,
  actualizarCierresDesdeAPI
} from '../services/api';

const CierresUF = () => {
  const [cierres, setCierres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [editingCierre, setEditingCierre] = useState(null);
  const [formData, setFormData] = useState({
    ciclo: '',
    uf_pesos: ''
  });
  const [importFile, setImportFile] = useState(null);
  const [importing, setImporting] = useState(false);
  const [updatingFromAPI, setUpdatingFromAPI] = useState(false);

  useEffect(() => {
    loadCierres();
  }, []);

  const loadCierres = async () => {
    try {
      setLoading(true);
      const data = await getCierresUF();
      setCierres(data);
    } catch (error) {
      console.error('Error loading cierres:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        uf_pesos: parseFloat(formData.uf_pesos)
      };

      if (editingCierre) {
        await updateCierreUF(editingCierre.id, payload);
      } else {
        await createCierreUF(payload);
      }
      
      setShowModal(false);
      setEditingCierre(null);
      resetForm();
      loadCierres();
    } catch (error) {
      console.error('Error saving cierre:', error);
      alert('Error al guardar cierre UF');
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
      await importarCierresUFJson(importFile);
      alert('Importación completada exitosamente');
      setShowImportModal(false);
      setImportFile(null);
      loadCierres();
    } catch (error) {
      console.error('Error importing cierres:', error);
      alert('Error al importar cierres: ' + error.message);
    } finally {
      setImporting(false);
    }
  };

  const handleUpdateFromAPI = async () => {
    if (!window.confirm('¿Actualizar cierres UF desde la API externa? Esto puede tomar unos segundos.')) {
      return;
    }
    try {
      setUpdatingFromAPI(true);
      await actualizarCierresDesdeAPI([2025, 2026]);
      alert('Actualización desde API completada exitosamente');
      loadCierres();
    } catch (error) {
      console.error('Error updating from API:', error);
      alert('Error al actualizar desde API: ' + error.message);
    } finally {
      setUpdatingFromAPI(false);
    }
  };

  const handleEdit = (cierre) => {
    setEditingCierre(cierre);
    setFormData({
      ciclo: cierre.ciclo,
      uf_pesos: cierre.uf_pesos
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este cierre UF?')) {
      try {
        await deleteCierreUF(id);
        loadCierres();
      } catch (error) {
        console.error('Error deleting cierre:', error);
        alert('Error al eliminar cierre UF');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      ciclo: '',
      uf_pesos: ''
    });
  };

  const filteredCierres = cierres.filter(c =>
    c.ciclo.includes(searchTerm)
  ).sort((a, b) => a.ciclo.localeCompare(b.ciclo));

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
          <h1 className="text-3xl font-bold text-foreground">Cierres UF</h1>
          <p className="text-muted-foreground">Valores de UF al cierre de cada mes</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleUpdateFromAPI}
            disabled={updatingFromAPI}
            className="flex items-center gap-2 rounded-lg border border-border px-4 py-2 text-sm font-medium text-foreground hover:bg-accent disabled:opacity-50"
          >
            <CloudDownload size={16} />
            {updatingFromAPI ? 'Actualizando...' : 'Actualizar desde API'}
          </button>
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
              setEditingCierre(null);
              setShowModal(true);
            }}
            className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
          >
            <Plus size={16} />
            Nuevo Cierre
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input
          type="text"
          placeholder="Buscar por ciclo (YYYYMM)..."
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
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Ciclo</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Valor UF (CLP)</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-muted-foreground">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filteredCierres.map((cierre) => (
                <tr key={cierre.id} className="border-t border-border hover:bg-accent/50">
                  <td className="px-4 py-3 text-sm font-medium text-foreground">{cierre.ciclo}</td>
                  <td className="px-4 py-3 text-sm text-foreground">$ {cierre.uf_pesos.toLocaleString('es-CL')}</td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => handleEdit(cierre)}
                        className="rounded p-1 hover:bg-accent hover:text-accent-foreground"
                      >
                        <Edit size={16} />
                      </button>
                      <button
                        onClick={() => handleDelete(cierre.id)}
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
        {filteredCierres.length === 0 && (
          <div className="p-8 text-center text-muted-foreground">
            No se encontraron cierres UF
          </div>
        )}
      </div>

      {/* Modal Crear/Editar */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-md rounded-lg bg-card p-6 shadow-lg">
            <h2 className="mb-4 text-xl font-bold text-foreground">
              {editingCierre ? 'Editar Cierre UF' : 'Nuevo Cierre UF'}
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
                <label className="mb-1 block text-sm font-medium text-foreground">Valor UF (CLP)</label>
                <input
                  type="number"
                  step="0.01"
                  required
                  value={formData.uf_pesos}
                  onChange={(e) => setFormData({ ...formData, uf_pesos: e.target.value })}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingCierre(null);
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
                  {editingCierre ? 'Actualizar' : 'Crear'}
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
            <h2 className="mb-4 text-xl font-bold text-foreground">Importar Cierres UF desde JSON</h2>
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

export default CierresUF;
