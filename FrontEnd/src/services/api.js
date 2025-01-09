import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api"; // ✅ Ensure correct API base URL
const ACCESS_TOKEN = "access";
const REFRESH_TOKEN = "refresh";

const api = axios.create({
    baseURL: API_BASE_URL
});

api.interceptors.request.use(
    async (config) => {
        let token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        
        // Handle expired access token (401 Unauthorized)
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const refreshToken = localStorage.getItem(REFRESH_TOKEN);
            if (refreshToken) {
                try {
                    const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
                        refresh: refreshToken,
                    });

                    localStorage.setItem(ACCESS_TOKEN, response.data.access);
                    originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
                    return api(originalRequest);
                } catch (err) {
                    console.error("Refresh token expired or invalid.");
                    localStorage.removeItem(ACCESS_TOKEN);
                    localStorage.removeItem(REFRESH_TOKEN);
                    window.location.href = "/login"; // Redirect to login
                }
            }
        }
        return Promise.reject(error);
    }
);

export default api;
