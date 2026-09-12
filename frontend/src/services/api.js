import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8001/api',
});

export const fetchStations = async () => {
  const response = await API.get('/stations');
  return response.data;
};

export const fetchGridConditions = async () => {
  const response = await API.get('/grid-conditions');
  return response.data;
};

export const optimizeCharging = async (payload) => {
  const response = await API.post('/optimize', payload);
  return response.data;
};
