import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: false,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
});

export default {
  getCells() {
    return apiClient.get('/cells/');
  },
  makeStep() {
    return apiClient.get('/step/');
  },
  resetSimulation() {
    return apiClient.get('/reset/');
  },
  changeParam(param, value) {
    return apiClient.get(`/change/${param}/${value}/`);
  },
  getParam(param) {
    return apiClient.get(`/get_param/${param}/`);
  }
}
