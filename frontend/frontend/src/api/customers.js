const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const getCustomers = async () => {
  const response = await fetch(`${API_URL}/customers`);
  if (!response.ok) throw new Error('Failed to fetch customers');
  return response.json();
};

export const getCustomer = async (id) => {
  const response = await fetch(`${API_URL}/customers/${id}`);
  if (!response.ok) throw new Error('Failed to fetch customer');
  return response.json();
};

export const createCustomer = async (customer) => {
  const response = await fetch(`${API_URL}/customers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(customer),
  });
  if (!response.ok) throw new Error('Failed to create customer');
  return response.json();
};

export const deleteCustomer = async (id) => {
  const response = await fetch(`${API_URL}/customers/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete customer');
  return response.json();
};

export const updateCustomer = async (id, customer) => {
  const response = await fetch(`${API_URL}/customers/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(customer),
  });
  if (!response.ok) throw new Error('Failed to update customer');
  return response.json();
};

export default {
  getCustomers,
  getCustomer,
  createCustomer,
  deleteCustomer,
  updateCustomer,
};
