"use client";

import { useEffect, useState } from "react";
import { BarChart3, FileText, Users, FlaskConical } from "lucide-react";
import { Sidebar } from "@/components/Sidebar";
import { LoginForm } from "@/components/LoginForm";
import { api } from "@/services/api";
import type { DashboardStats } from "@/types";

export default function AdminPage() {
  const [authed, setAuthed] = useState(false);
  const [role, setRole] = useState<string>();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [evalResult, setEvalResult] = useState<Record<string, unknown> | null>(null);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if (localStorage.getItem("token")) {
      setAuthed(true);
      const r = localStorage.getItem("role") || "viewer";
      setRole(r);
      if (r === "admin" || r === "analyst") {
        api.adminStats().then(setStats).catch(() => {});
      }
    }
  }, []);

  async function runEval() {
    setRunning(true);
    try {
      const res = await api.runEvaluation();
      setEvalResult(res.metrics);
    } finally {
      setRunning(false);
    }
  }

  if (!authed) return <LoginForm onLogin={() => setAuthed(true)} />;

  const cards = [
    { label: "Users", value: stats?.total_users ?? "—", icon: Users },
    { label: "Documents", value: stats?.total_documents ?? "—", icon: FileText },
    { label: "Indexed", value: stats?.indexed_documents ?? "—", icon: BarChart3 },
    { label: "Evaluations", value: stats?.total_evaluations ?? "—", icon: FlaskConical },
  ];

  return (
    <div className="flex h-screen">
      <Sidebar role={role} />
      <main className="flex-1 p-8 overflow-y-auto">
        <h2 className="text-xl font-semibold mb-8">Admin Dashboard</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {cards.map(({ label, value, icon: Icon }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <Icon className="w-5 h-5 text-brand-500 mb-3" />
              <p className="text-2xl font-bold">{value}</p>
              <p className="text-xs text-slate-500 mt-1">{label}</p>
            </div>
          ))}
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h3 className="font-medium mb-4">Evaluation Pipeline</h3>
          <button
            onClick={runEval}
            disabled={running}
            className="bg-brand-500 hover:bg-brand-600 disabled:opacity-50 px-4 py-2 rounded-lg text-sm"
          >
            {running ? "Running..." : "Run Sample Evaluation"}
          </button>
          {evalResult && (
            <pre className="mt-4 bg-slate-950 rounded-lg p-4 text-xs overflow-x-auto text-green-400">
              {JSON.stringify(evalResult, null, 2)}
            </pre>
          )}
        </div>
      </main>
    </div>
  );
}
