import { api } from "./api";

export async function updateTest(testId, payload) {
  const { data } = await api.patch(`/tests/${testId}`, payload);
  return data;
}

export async function deleteTest(testId) {
  await api.delete(`/tests/${testId}`);
}

//get subject_tests to show them on testoverview
export async function getTestsBySubject(subjectId) {
  const { data } = await api.get(`/subject-tests/bySubject/${subjectId}`);
  return data;
}
