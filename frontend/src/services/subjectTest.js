import { api } from "./api";

// export async function createSubjectTest(name, subject_id, questionTyp_select, question_count) {
//   const payload = { name, subject_id, questionTyp_select, question_count };
//   console.log("createSubjectTest payload ->", payload);
//   await api.post("/subjecttests/{questionTyp_select}", payload);
// }

// export async function createSubjectTest(name, subject_id, questionTyp_select, question_count) {
//   const payload = { name, subject_id, question_count };
//   console.log("createSubjectTest payload ->", payload);
//   console.log("questionTyp -> ", questionTyp_select);
//   await api.post(`/subjecttests/${questionTyp_select}`, payload);
// }

export async function createSubjectTest(file, name, subject_id, questionTyp_select, question_count) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);
  formData.append("subject_id", subject_id);
  formData.append("question_count", question_count);

  await api.post(`/subjecttests/${questionTyp_select}`, formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
}

// export async function patchUser(userId, payload) {
//   const { data } = await api.patch(`/users/${userId}`, payload);
//   return data;
// }

export async function getTestsBySubject(subjectId) {
  const { data } = await api.get(`/subjecttests/bySubject/${subjectId}`);
  return data;
}

export async function updateTest(testId, payload) {
  const { data } = await api.patch(`/tests/${testId}`, payload);
  return data;
}

export async function deleteTest(testId) {
  await api.delete(`/tests/${testId}`);
}
