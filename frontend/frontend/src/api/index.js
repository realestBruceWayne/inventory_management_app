const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export { default as productsAPI } from './products';
export { default as customersAPI } from './customers';
export { default as ordersAPI } from './orders';
export { default as dashboardAPI } from './dashboard';
