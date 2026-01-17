import { api } from "./api";

// export async function createSubjectTest(name, subject_id, questionTyp_select, question_count) {
//   const payload = { name, subject_id, questionTyp_select, question_count };
//   console.log("createSubjectTest payload ->", payload);
//   await api.post("/subjecttests/{questionTyp_select}", payload);
// }

export async function createSubjectTest(name, subject_id, questionTyp_select, question_count) {
  const payload = { name, subject_id, question_count };
  console.log("createSubjectTest payload ->", payload);
  console.log("questionTyp -> ", questionTyp_select);
  await api.post(`/subjecttests/${questionTyp_select}`, payload);
}

// export async function patchUser(userId, payload) {
//   const { data } = await api.patch(`/users/${userId}`, payload);
//   return data;
// }
