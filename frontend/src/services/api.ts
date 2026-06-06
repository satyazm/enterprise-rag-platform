const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };
  if (token) headers.Authorization = `Bearer ${token}`;
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export const api = {
  login: (email: string, password: string) => {
    const body = new URLSearchParams({ username: email, password });
    return fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    }).then(async (res) => {
      if (!res.ok) throw new Error("Invalid credentials");
      return res.json();
    });
  },

  me: () => request<{ id: string; email: string; full_name: string; role: string }>("/auth/me"),

  chat: (message: string, conversationId?: string) =>
    request<{ conversation_id: string; message: string; citations: unknown[]; trace_id?: string }>(
      "/chat",
      { method: "POST", body: JSON.stringify({ message, conversation_id: conversationId }) }
    ),

  conversations: () =>
    request<{ id: string; title: string; updated_at: string }[]>("/chat/conversations"),

  messages: (id: string) =>
    request<{ role: string; content: string; citations: unknown[]; created_at: string }[]>(
      `/chat/conversations/${id}/messages`
    ),

  documents: () => request<import("@/types").Document[]>("/documents"),

  uploadDocument: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<import("@/types").Document>("/documents/upload", { method: "POST", body: form });
  },

  adminStats: () => request<import("@/types").DashboardStats>("/admin/stats"),

  runEvaluation: (datasetName = "sample") =>
    request<{ dataset: string; metrics: Record<string, unknown> }>("/admin/evaluate", {
      method: "POST",
      body: JSON.stringify({ dataset_name: datasetName }),
    }),
};
