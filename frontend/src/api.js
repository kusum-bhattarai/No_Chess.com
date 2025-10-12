import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const apiClient = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
});

export default apiClient;