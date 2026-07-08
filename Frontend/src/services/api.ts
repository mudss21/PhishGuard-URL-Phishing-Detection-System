import axios from "axios";

// Backend base URL (WITHOUT /predict)
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "https://project-api-1-hso8.onrender.com";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Optional JWT token support
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// =====================================================
// TYPES
// =====================================================

export interface PredictionResult {
  prediction: string;
  probability: number;
}

export interface HistoryEntry {
  url: string;
  result: "Phishing" | "Safe";
  confidence: number;
  timestamp: string;
}

// =====================================================
// API CALLS
// =====================================================

export const predictURL = async (
  url: string
): Promise<PredictionResult> => {
  const { data } = await api.post<PredictionResult>(
    "/predict",
    { url }
  );

  return data;
};

export const getHistory = async (): Promise<HistoryEntry[]> => {
  const { data } = await api.get<HistoryEntry[]>("/history");
  return data;
};

export const login = async (
  username: string,
  password: string
) => {
  const { data } = await api.post("/login", {
    username,
    password,
  });

  if (data.token) {
    localStorage.setItem("token", data.token);
  }

  return data;
};

export default api;