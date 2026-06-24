const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const getDashboardSummary = async () => {
  const response = await fetch(`${API_URL}/dashboard/summary`);
  if (!response.ok) throw new Error('Failed to fetch dashboard summary');
  return response.json();
};

export default {
  getDashboardSummary,
};
