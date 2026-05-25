import axios from "axios";
import logger from "./logger";


const baseURL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const API = axios.create({
    baseURL: baseURL.endsWith('/') ? `${baseURL}api` : `${baseURL}/api`,
});

API.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
        config.headers.Authorization = "Bearer " + token;
    }
    return config;
});

API.interceptors.response.use(
    (response) => {
        logger.info(`API ${response.config.method.toUpperCase()} ${response.config.url} — ${response.status}`);
        return response;
    },
    (error) => {
        logger.error(`API ERROR ${error.config?.method?.toUpperCase()} ${error.config?.url} — ${error.response?.status}`, error);
        if (error.response?.status === 401) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
        }
        return Promise.reject(error);
    }
);

export default API;