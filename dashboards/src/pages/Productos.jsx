import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Search, RefreshCw } from 'lucide-react';
import {
  getProductos,
  createProducto,
  updateProducto,
  deleteProducto
} from '../services/api';

const Productos = () => {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingProducto, setEditingProducto] = useState(null);
  const [formData, setFormData] = useState({
    codigo_erp: '',
    nombre: '',
    peso_ton: '',
    peso_gr: '',
    codigo_interno: '',
    categoria: '',
    subcategoria: '',
    tipo_material: '',
    material: '',
    riesgo: ''
  });

  useEffect(() => {
    loadProductos();
  }, []);

  const loadProductos = async () => {
    try {
      setLoading(true);
      const data = await getProductos();
      setProductos(data);
    } catch (error) {
      console.error('Error loading productos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        peso_ton: parseFloat(formData.peso_ton),
        peso_gr: parseFloat(formData.peso_gr),
        codigo_interno: parseInt(formData.codigo_interno)
      };

      if (editingProducto) {
        await updateProducto(editingProducto.id, payload);
      } else {
        await createProducto(payload);
      }
      
      setShowModal(false);
      setEditingProducto(null);
      resetForm();
      loadProductos();
    } catch (error) {
      console.error('Error saving producto:', error);
      alert('Error al guardar producto');
    }
  };

  const handleEdit = (producto) => {
    setEditingProducto(producto);
    setFormData({
      codigo_erp: producto.codigo_erp,
      nombre: producto.nombre,
      peso_ton: producto.peso_ton,
      peso_gr: producto.peso_gr,
      codigo_interno: producto.codigo_interno,
      categoria: producto.categoria,
      subcategoria: producto.subcategoria,
      tipo_material: producto.tipo_material,
      material: producto.material,
      riesgo: producto.riesgo
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este producto?')) {
      try {
        await deleteProducto(id);
        loadProductos();
      } catch (error) {
        console.error('Error deleting producto:', error);
        alert('Error al eliminar producto');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      codigo_erp: '',
      nombre: '',
      peso_ton: '',
      peso_gr: '',
      codigo_interno: '',
      categoria: '',
      subcategoria: '',
      tipo_material: '',
      material: '',
      riesgo: ''
    });
  };

  const filteredProductos = productos.filter(p =>
    p.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.codigo_erp.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.categoria.toLowerCase().includes(searchTerm.toLowerCase())
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
          <h1 className="text-3xl font-bold text-foreground">Productos</h1>
          <p className="text-muted-foreground">Gestión de productos de reciclaje</p>
        </div>
        <button
          onClick={() => {
            resetForm();
            setEditingProducto(null);
            setShowModal(true);
          }}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          <Plus size={16} />
          Nuevo Producto
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input
          type="text"
          placeholder="Buscar por nombre, código o categoría..."
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
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Código ERP</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Nombre</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Código Interno</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Categoría</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Peso (ton)</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Peso (gr)</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Material</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Riesgo</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-muted-foreground">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filteredProductos.map((producto) => (
                <tr key={producto.id} className="border-t border-border hover:bg-accent/50">
                  <td className="px-4 py-3 text-sm text-foreground">{producto.codigo_erp}</td>
                  <td className="px-4 py-3 text-sm font-medium text-foreground">{producto.nombre}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{producto.codigo_interno}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{producto.categoria}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{producto.peso_ton.toFixed(5)}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{producto.peso_gr}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{producto.material}</td>
                  <td className="px-4 py-3 text-sm text-foreground">{producto.riesgo}</td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => handleEdit(producto)}
                        className="rounded p-1 hover:bg-accent hover:text-accent-foreground"
                      >
                        <Edit size={16} />
                      </button>
                      <button
                        onClick={() => handleDelete(producto.id)}
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
        {filteredProductos.length === 0 && (
          <div className="p-8 text-center text-muted-foreground">
            No se encontraron productos
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-2xl rounded-lg bg-card p-6 shadow-lg">
            <h2 className="mb-4 text-xl font-bold text-foreground">
              {editingProducto ? 'Editar Producto' : 'Nuevo Producto'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
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
                  <label className="mb-1 block text-sm font-medium text-foreground">Nombre</label>
                  <input
                    type="text"
                    required
                    value={formData.nombre}
                    onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-foreground">Código Interno</label>
                  <input
                    type="number"
                    required
                    value={formData.codigo_interno}
                    onChange={(e) => setFormData({ ...formData, codigo_interno: e.target.value })}
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-foreground">Categoría</label>
                  <input
                    type="text"
                    required
                    value={formData.categoria}
                    onChange={(e) => setFormData({ ...formData, categoria: e.target.value })}
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-foreground">Subcategoría</label>
                  <input
                    type="text"
                    value={formData.subcategoria}
                    onChange={(e) => setFormData({ ...formData, subcategoria: e.target.value })}
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-foreground">Tipo Material</label>
                  <input
                    type="text"
                    value={formData.tipo_material}
                    onChange={(e) => setFormData({ ...formData, tipo_material: e.target.value })}
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-foreground">Material</label>
                  <input
                    type="text"
                    value={formData.material}
                    onChange={(e) => setFormData({ ...formData, material: e.target.value })}
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-foreground">Riesgo</label>
                  <input
                    type="text"
                    value={formData.riesgo}
                    onChange={(e) => setFormData({ ...formData, riesgo: e.target.value })}
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-foreground">Peso (toneladas)</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={formData.peso_ton}
                    onChange={(e) => setFormData({ ...formData, peso_ton: e.target.value })}
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium text-foreground">Peso (gramos)</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={formData.peso_gr}
                    onChange={(e) => setFormData({ ...formData, peso_gr: e.target.value })}
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                </div>
              </div>
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingProducto(null);
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
                  {editingProducto ? 'Actualizar' : 'Crear'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Productos;
