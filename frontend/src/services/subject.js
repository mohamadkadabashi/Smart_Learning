import { api } from "./api";

export async function createSubject({ name, user_id }) {
  const { data } = await api.post("/subjects", { name, user_id });
  return data; 
}

export async function getUserSubjects({ user_id }) {
  const { data } = await api.get(`/subjects/byUser/${user_id}`);
  return { data };
}

export async function getSubjects() {
  const { data } = await api.get("/subjects/mySubjects");
  return data;
}

export async function getSubjectById(subjectId) {
  const { data } = await api.get(`/subjects/${subjectId}`);
  return data;
}

export async function updateSubject(subjectId, payload) {
  const { data } = await api.patch(`/subjects/${subjectId}`, payload);
  return data;
}

export async function deleteSubject(subjectId) {
  return await api.delete(`/subjects/${subjectId}`);
}

