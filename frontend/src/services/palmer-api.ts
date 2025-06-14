import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' ? 'https://palmer-apps.com' : 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' }
});

export const chat = async (message: string, distributorId: string = 'demo-001') => {
  const { data } = await api.post('/palmer/chat', { distributor_id: distributorId, message });
  return data;
};

export const uploadAndChat = async (file: File, message: string, distributorId: string = 'demo-001') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('distributor_id', distributorId);
  formData.append('message', message);
  const { data } = await api.post('/palmer/upload-and-chat', formData);
  return data;
};

export const health = () => api.get('/health');
