"use client";

import { useEffect, useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { ChatWindow } from "@/components/ChatWindow";
import { LoginForm } from "@/components/LoginForm";

export default function Home() {
  const [authed, setAuthed] = useState(false);
  const [role, setRole] = useState<string>();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setAuthed(true);
      setRole(localStorage.getItem("role") || "viewer");
    }
  }, []);

  if (!authed) return <LoginForm onLogin={() => { setAuthed(true); setRole(localStorage.getItem("role") || "viewer"); }} />;

  return (
    <div className="flex h-screen">
      <Sidebar role={role} />
      <main className="flex-1 flex flex-col">
        <header className="border-b border-slate-800 px-6 py-4 flex items-center justify-between">
          <h2 className="font-semibold">Knowledge Assistant</h2>
          <span className="text-xs bg-slate-800 px-3 py-1 rounded-full text-slate-400 capitalize">{role}</span>
        </header>
        <ChatWindow />
      </main>
    </div>
  );
}
