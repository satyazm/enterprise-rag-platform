"use client";

import { useState } from "react";
import { api } from "@/services/api";

export function LoginForm({ onLogin }: { onLogin: () => void }) {
  const [email, setEmail] = useState("admin@enterprise.local");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await api.login(email, password);
      localStorage.setItem("token", res.access_token);
      localStorage.setItem("role", res.role);
      onLogin();
    } catch {
      setError("Invalid credentials");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950">
      <form onSubmit={handleSubmit} className="bg-slate-900 border border-slate-800 rounded-2xl p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-2">Enterprise RAG</h2>
        <p className="text-slate-400 text-sm mb-6">Sign in to the internal knowledge platform</p>
        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 mb-3 text-sm"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 mb-6 text-sm"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-brand-500 hover:bg-brand-600 rounded-lg py-3 font-medium text-sm transition-colors"
        >
          {loading ? "Signing in..." : "Sign In"}
        </button>
        <p className="text-xs text-slate-500 mt-4 text-center">
          Demo: admin@enterprise.local / admin123
        </p>
      </form>
    </div>
  );
}
