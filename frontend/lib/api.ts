export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export function authHeaders(token?: string) {
  const h: Record<string, string> = { "Content-Type": "application/json" };
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

export async function login(email: string, password: string) {
  const body = new URLSearchParams();
  body.set("username", email);
  body.set("password", password);
  const res = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function register(email: string, password: string, full_name?: string) {
  const res = await fetch(`${API_URL}/api/v1/auth/register`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ email, password, full_name }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function me(token: string) {
  const res = await fetch(`${API_URL}/api/v1/users/me`, {
    headers: authHeaders(token),
    cache: "no-store",
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function createTask(token: string, type: string, payload: any) {
  const res = await fetch(`${API_URL}/api/v1/tasks/`, {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify({ type, payload }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getTask(token: string, id: number) {
  const res = await fetch(`${API_URL}/api/v1/tasks/${id}`, {
    headers: authHeaders(token),
    cache: "no-store",
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
