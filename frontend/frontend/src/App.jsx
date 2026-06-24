import React, { useState, useEffect } from 'react';
import { AlertCircle, LogOut } from 'lucide-react';
import { productsAPI, customersAPI, ordersAPI, dashboardAPI } from './api';
import Header from './components/Header';
import Navigation from './components/Navigation';
import DashboardView from './components/DashboardView';
import ProductsView from './components/ProductsView';
import CustomersView from './components/CustomersView';
import OrdersView from './components/OrdersView';
import Loading from './components/Loading';
import Login from './components/Login';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [products, setProducts] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
      loadData();
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
    loadData();
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setProducts([]);
    setCustomers([]);
    setOrders([]);
    setDashboard(null);
  };

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [productsData, customersData, ordersData, dashboardData] = await Promise.all([
        productsAPI.getProducts(),
        customersAPI.getCustomers(),
        ordersAPI.getOrders(),
        dashboardAPI.getDashboardSummary(),
      ]);
      setProducts(productsData);
      setCustomers(customersData);
      setOrders(ordersData);
      setDashboard(dashboardData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 text-gray-800">
      <Header error={error} />
      <div className="flex justify-between items-center px-4 sm:px-6 lg:px-8 py-4 bg-white border-b">
        <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
        <button
          onClick={handleLogout}
          className="flex items-center px-4 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-md"
        >
          <LogOut className="h-4 w-4 mr-2" />
          Logout
        </button>
      </div>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading && <Loading />}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <AlertCircle className="h-5 w-5 text-red-600 mr-2" />
              <p className="text-red-800">{error}</p>
            </div>
            <button onClick={loadData} className="mt-2 text-sm text-red-600 hover:text-red-800 underline">
              Retry
            </button>
          </div>
        )}

        {!loading && !error && (
          <>
            {activeTab === 'dashboard' && <DashboardView dashboard={dashboard} products={products} />}
            {activeTab === 'products' && <ProductsView products={products} onRefresh={loadData} />}
            {activeTab === 'customers' && <CustomersView customers={customers} onRefresh={loadData} />}
            {activeTab === 'orders' && <OrdersView orders={orders} onRefresh={loadData} />}
          </>
        )}
      </main>
    </div>
  );
}
