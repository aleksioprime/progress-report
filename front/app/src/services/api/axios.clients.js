import axios from "axios";

export const authClient = axios.create({
  baseURL: import.meta.env.VITE_AUTH_URL, // Хост для авторизации
});

export const backendClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL, // Хост для остальных запросов
});
