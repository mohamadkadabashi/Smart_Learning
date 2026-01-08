import { api } from "./api";

/**
 * subject_create must match your FastAPI SubjectCreate schema:
 * { name: string, user_id: number }
 */
export async function createSubject({ name, user_id }) {
  const { data } = await api.post("/subjects", { name, user_id });
  return data; // SubjectRead from backend
}
