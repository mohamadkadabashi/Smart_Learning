import { api } from "./api";

export async function createSubject({ name, user_id }) {
  const { data } = await api.post("/subjects", { name, user_id });
  return data; // SubjectRead from backend
}

export async function getUserSubjects({ user_id }) {
  const { data } = await api.get(`/subjects/byUser/${user_id}`);
  return { data };
}
