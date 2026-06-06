export interface User {
  id: string;
  email: string;
  full_name: string;
  role: "admin" | "analyst" | "viewer";
}

export interface Citation {
  document_id: string;
  document_title: string;
  chunk_index: number;
  excerpt: string;
  score: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
}

export interface Document {
  id: string;
  title: string;
  filename: string;
  file_type: string;
  status: string;
}

export interface DashboardStats {
  total_users: number;
  total_documents: number;
  indexed_documents: number;
  total_evaluations: number;
}
