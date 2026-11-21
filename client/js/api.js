import { API_BASE_URL } from "./config.js";

const ACCESS_KEY = "autocare_access";
const REFRESH_KEY = "autocare_refresh";

export const tokenStore = {
  access: () => sessionStorage.getItem(ACCESS_KEY),
  refresh: () => sessionStorage.getItem(REFRESH_KEY),
  save: ({ access, refresh }) => {
    if (access) sessionStorage.setItem(ACCESS_KEY, access);
    if (refresh) sessionStorage.setItem(REFRESH_KEY, refresh);
  },
  clear: () => {
    sessionStorage.removeItem(ACCESS_KEY);
    sessionStorage.removeItem(REFRESH_KEY);
    sessionStorage.removeItem("autocare_user");
  }
};

async function decodeResponse(response) {
  const type = response.headers.get("content-type") || "";
  const body = type.includes("application/json") ? await response.json() : await response.text();
  if (!response.ok) {
    const detail = typeof body === "string" ? body : body.detail || body.message || body;
    const error = new Error(typeof detail === "string" ? detail : "The request could not be completed.");
    error.status = response.status;
    error.data = body;
    throw error;
  }
  return body;
}

async function refreshAccess() {
  const refresh = tokenStore.refresh();
  if (!refresh) return false;
  const response = await fetch(`${API_BASE_URL}/api/auth/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh })
  });
  if (!response.ok) {
    tokenStore.clear();
    return false;
  }
  const tokens = await response.json();
  tokenStore.save(tokens);
  return Boolean(tokens.access);
}

export async function api(path, options = {}) {
  const { method = "GET", body, auth = true, retry = true, headers = {} } = options;
  const requestHeaders = new Headers(headers);
  if (auth && tokenStore.access()) requestHeaders.set("Authorization", `Bearer ${tokenStore.access()}`);
  let payload = body;
  if (body !== undefined && !(body instanceof FormData) && !(body instanceof Blob)) {
    requestHeaders.set("Content-Type", "application/json");
    payload = JSON.stringify(body);
  }
  let response = await fetch(`${API_BASE_URL}${path}`, { method, headers: requestHeaders, body: payload });
  if (response.status === 401 && auth && retry && await refreshAccess()) {
    requestHeaders.set("Authorization", `Bearer ${tokenStore.access()}`);
    response = await fetch(`${API_BASE_URL}${path}`, { method, headers: requestHeaders, body: payload });
  }
  if (response.status === 401 && auth) tokenStore.clear();
  return decodeResponse(response);
}

export function listFrom(data) {
  return Array.isArray(data) ? data : Array.isArray(data?.results) ? data.results : [];
}

export function queryString(values = {}) {
  const params = new URLSearchParams();
  Object.entries(values).forEach(([key, value]) => {
    if (value !== "" && value !== null && value !== undefined) params.set(key, value);
  });
  const query = params.toString();
  return query ? `?${query}` : "";
}
