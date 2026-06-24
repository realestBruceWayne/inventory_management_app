const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const getOrders = async () => {
  const response = await fetch(`${API_URL}/orders`);
  if (!response.ok) throw new Error('Failed to fetch orders');
  return response.json();
};

export const getOrder = async (id) => {
  const response = await fetch(`${API_URL}/orders/${id}`);
  if (!response.ok) throw new Error('Failed to fetch order');
  return response.json();
};

export const createOrder = async (order) => {
  const response = await fetch(`${API_URL}/orders`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(order),
  });
  if (!response.ok) throw new Error('Failed to create order');
  return response.json();
};

export const deleteOrder = async (id) => {
  const response = await fetch(`${API_URL}/orders/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete order');
  return response.json();
};

export default {
  getOrders,
  getOrder,
  createOrder,
  deleteOrder,
};
