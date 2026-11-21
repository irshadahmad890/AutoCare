import { api, tokenStore } from "./api.js";

export async function login(username, password) {
  const tokens = await api("/api/auth/login/", {
    method: "POST", auth: false, body: { username, password }
  });
  tokenStore.save(tokens);
  const user = await api("/api/auth/me/");
  sessionStorage.setItem("autocare_user", JSON.stringify(user));
  return user;
}

export async function registerCustomer(values) {
  return api("/api/auth/register/", { method: "POST", auth: false, body: values });
}

export function currentUser() {
  try { return JSON.parse(sessionStorage.getItem("autocare_user") || "null"); }
  catch { return null; }
}

export async function loadCurrentUser() {
  const user = await api("/api/auth/me/");
  sessionStorage.setItem("autocare_user", JSON.stringify(user));
  return user;
}

export function logout() {
  tokenStore.clear();
  window.location.href = "./login.html";
}
