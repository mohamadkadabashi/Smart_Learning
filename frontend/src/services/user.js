import Vue from "vue";
import { api } from "./api";
import router from '@/router/index.js';

export const authState = Vue.observable({
  loggedIn: false,
});

function initAuthFromStorage() {
  const token = localStorage.getItem("access_token");
  const expiresAt = localStorage.getItem("access_token_expires_at");
  authState.loggedIn = Boolean(token && expiresAt && Date.now() <= Number(expiresAt));
}
initAuthFromStorage();

export async function register(username, email, password) {
  const payload = { username, email, password };
  console.log("REGISTER payload ->", payload);
  await api.post("/users/register", payload);
}

export async function login(identifier, password) {
  const body = new URLSearchParams();
  body.append("username", identifier);
  body.append("password", password);

  const response = await api.post("/users/login", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  const expiresInMs = response.data.expires_in_minutes * 60 * 1000;
  const expiresAt = Date.now() + expiresInMs;

  localStorage.setItem("access_token", response.data.access_token);
  localStorage.setItem("access_token_expires_at", expiresAt.toString());

  authState.loggedIn = true;

  return response.data;
}

export async function getMe() {
  const { data } = await api.get("/users/me");
  return data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("access_token_expires_at");
  localStorage.removeItem("user_id");

  authState.loggedIn = false;

  router.push("/").catch(() => {});
}

export async function patchUser(userId, payload) {
  const { data } = await api.patch(`/users/${userId}`, payload);
  return data;
}

export function isAuthenticated() {
  const token = localStorage.getItem("access_token");
  const expiresAt = localStorage.getItem("access_token_expires_at");

  if (!token || !expiresAt) {
    authState.loggedIn = false;
    return false;
  }

  if (Date.now() > Number(expiresAt)) {
    logout();
    return false;
  }

  authState.loggedIn = true;
  return true;
}

