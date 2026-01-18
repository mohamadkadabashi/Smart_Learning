import { api } from "./api";

export async function startAttempt(payload) {
  const { data } = await api.post("/attempts/start", payload);
  return data;
}

export async function finishAttempt(attemptId, payload) {
  const { data } = await api.post(`/attempts/${attemptId}/finish`, payload);
  return data;
}
