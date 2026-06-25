import React, { useState } from 'react';
import { Plus } from 'lucide-react';
import { ordersAPI, customersAPI, productsAPI } from '../api';
import Modal from './Modal';

export default function OrdersView({ orders, onRefresh }) {
  const [showAddModal, setShowAddModal] = useState(false);
  const [formData, setFormData] = useState({ customer_id: '', product_id: '', quantity: '' });
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [addError, setAddError] = useState('');

  const loadDropdownData = async () => {
    try {
      const [customersData, productsData] = await Promise.all([customersAPI.getCustomers(), productsAPI.getProducts()]);
      setCustomers(customersData);
      setProducts(productsData);
    } catch (err) {
      console.error('Failed to load dropdown data:', err);
    }
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    setAddError('');
    try {
      await ordersAPI.createOrder({
        customer_id: parseInt(formData.customer_id),
        product_id: parseInt(formData.product_id),
        quantity: parseInt(formData.quantity),
      });
      setShowAddModal(false);
      setFormData({ customer_id: '', product_id: '', quantity: '' });
      onRefresh();
    } catch (err) {
      setAddError(err.message);
    }
  };

  const openAddModal = async () => {
    await loadDropdownData();
    setShowAddModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this order?')) {
      try {
        await ordersAPI.deleteOrder(id);
        onRefresh();
      } catch (err) {
        alert(err.message);
      }
    }
  };

  return (
    <>
      <div className="sm:flex sm:items-center sm:justify-between mb-6">
        <div>
          <h2 className="text-lg font-semibold text-gray-900">Order Management</h2>
          <p className="text-sm text-gray-500 mt-1">Track and manage customer orders.</p>
        </div>
        <button
          onClick={openAddModal}
          className="mt-4 sm:mt-0 inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg shadow-sm transition-colors text-sm"
        >
          <Plus className="h-4 w-4" /> Create Order
        </button>
      </div>

      <div className="bg-white/80 backdrop-blur-lg rounded-2xl border border-gray-200/50 shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gradient-to-r from-gray-50 to-green-50 border-b border-gray-200/50 text-xs font-semibold uppercase tracking-wider text-gray-600">
                <th className="py-4 px-6">Order ID</th>
                <th className="py-4 px-6">Customer</th>
                <th className="py-4 px-6">Product</th>
                <th className="py-4 px-6">Quantity</th>
                <th className="py-4 px-6">Total</th>
                <th className="py-4 px-6 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 text-sm">
              {orders.map((order) => (
                <tr key={order.id} className="hover:bg-green-50/50 transition-colors">
                  <td className="py-4 px-6 font-mono text-xs text-gray-600 bg-gray-50/50">#{order.id}</td>
                  <td className="py-4 px-6 font-medium text-gray-900">{order.customer?.full_name || 'Unknown'}</td>
                  <td className="py-4 px-6 text-gray-600">{order.product?.name || 'Unknown'}</td>
                  <td className="py-4 px-6 text-gray-600">{order.quantity}</td>
                  <td className="py-4 px-6 font-semibold text-gray-900">${order.total_amount.toFixed(2)}</td>
                  <td className="py-4 px-6 text-right">
                    <button
                      onClick={() => handleDelete(order.id)}
                      className="inline-flex items-center px-3 py-1.5 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {showAddModal && (
        <Modal onClose={() => setShowAddModal(false)} title="Create Order">
          <form onSubmit={handleAdd} className="space-y-5">
            {addError && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {addError}
              </div>
            )}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Customer</label>
              <select
                required
                value={formData.customer_id}
                onChange={(e) => setFormData({ ...formData, customer_id: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              >
                <option value="">Select a customer</option>
                {customers.map((customer) => (
                  <option key={customer.id} value={customer.id}>
                    {customer.full_name} ({customer.email})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Product</label>
              <select
                required
                value={formData.product_id}
                onChange={(e) => setFormData({ ...formData, product_id: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              >
                <option value="">Select a product</option>
                {products.map((product) => (
                  <option key={product.id} value={product.id}>
                    {product.name} (${product.price.toFixed(2)}) - {product.quantity} in stock
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Quantity</label>
              <input
                type="number"
                required
                min="1"
                placeholder="Enter quantity"
                value={formData.quantity}
                onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              />
            </div>
            <div className="flex justify-end gap-3 pt-4">
              <button
                type="button"
                onClick={() => setShowAddModal(false)}
                className="px-6 py-2.5 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-xl font-medium transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-6 py-2.5 text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-xl font-medium transition-all shadow-md hover:shadow-lg"
              >
                Create Order
              </button>
            </div>
          </form>
        </Modal>
      )}
    </>
  );
}
