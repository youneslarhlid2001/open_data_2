import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const API_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT_MS || 180000); // 3 min pour laisser le pipeline s'exécuter

const client = axios.create({
  baseURL: API_URL,
  timeout: API_TIMEOUT,
});

export const runPipeline = async () => {
  const { data } = await client.post("/run");
  return data;
};

export const fetchPreview = async (limit = 50) => {
  const { data } = await client.get("/preview", { params: { limit } });
  return data;
};

export const fetchStats = async () => {
  const { data } = await client.get("/stats");
  return data;
};

export const downloadParquet = () => {
  window.open(`${API_URL}/download`, "_blank");
};

