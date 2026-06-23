import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Productos from './pages/Productos';
import Ventas from './pages/Ventas';
import Tarifas from './pages/Tarifas';
import CierresUF from './pages/CierresUF';
import DataProcesada from './pages/DataProcesada';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="productos" element={<Productos />} />
          <Route path="ventas" element={<Ventas />} />
          <Route path="tarifas" element={<Tarifas />} />
          <Route path="cierres-uf" element={<CierresUF />} />
          <Route path="data-procesada" element={<DataProcesada />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
