import { api } from "./api";

export async function createSubject({ name, user_id }) {
  const { data } = await api.post("/subjects", { name, user_id });
  return data; // SubjectRead from backend
}
