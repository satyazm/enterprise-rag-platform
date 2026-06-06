"use client";

import { useEffect, useState } from "react";
import { Upload, FileText } from "lucide-react";
import { Sidebar } from "@/components/Sidebar";
import { LoginForm } from "@/components/LoginForm";
import { api } from "@/services/api";
import type { Document } from "@/types";

export default function DocumentsPage() {
  const [authed, setAuthed] = useState(false);
  const [role, setRole] = useState<string>();
  const [docs, setDocs] = useState<Document[]>([]);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    if (localStorage.getItem("token")) {
      setAuthed(true);
      setRole(localStorage.getItem("role") || "viewer");
      api.documents().then(setDocs).catch(() => {});
    }
  }, []);

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      const doc = await api.uploadDocument(file);
      setDocs((d) => [doc, ...d]);
    } finally {
      setUploading(false);
    }
  }

  if (!authed) return <LoginForm onLogin={() => setAuthed(true)} />;

  const canUpload = role === "admin" || role === "analyst";

  return (
    <div className="flex h-screen">
      <Sidebar role={role} />
      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-xl font-semibold">Document Library</h2>
          {canUpload && (
            <label className="flex items-center gap-2 bg-brand-500 hover:bg-brand-600 px-4 py-2 rounded-lg cursor-pointer text-sm">
              <Upload className="w-4 h-4" />
              {uploading ? "Uploading..." : "Upload Document"}
              <input type="file" className="hidden" accept=".pdf,.docx,.pptx,.html,.txt,.md" onChange={handleUpload} />
            </label>
          )}
        </div>
        <div className="grid gap-3">
          {docs.map((doc) => (
            <div key={doc.id} className="flex items-center gap-4 bg-slate-900 border border-slate-800 rounded-xl p-4">
              <FileText className="w-5 h-5 text-brand-500" />
              <div className="flex-1">
                <p className="font-medium text-sm">{doc.title}</p>
                <p className="text-xs text-slate-500">{doc.file_type.toUpperCase()}</p>
              </div>
              <span className={`text-xs px-3 py-1 rounded-full ${
                doc.status === "indexed" ? "bg-green-500/20 text-green-400" :
                doc.status === "processing" ? "bg-yellow-500/20 text-yellow-400" :
                "bg-slate-700 text-slate-400"
              }`}>
                {doc.status}
              </span>
            </div>
          ))}
          {docs.length === 0 && (
            <p className="text-slate-500 text-center py-12">No documents indexed yet</p>
          )}
        </div>
      </main>
    </div>
  );
}
