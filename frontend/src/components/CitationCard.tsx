import type { Citation } from "@/types";

export function CitationCard({ citation, index }: { citation: Citation; index: number }) {
  return (
    <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-3 text-xs">
      <div className="flex items-center justify-between mb-1">
        <span className="font-medium text-brand-500">[{index}] {citation.document_title}</span>
        <span className="text-slate-500">score: {citation.score.toFixed(2)}</span>
      </div>
      <p className="text-slate-400 line-clamp-2">{citation.excerpt}</p>
    </div>
  );
}
