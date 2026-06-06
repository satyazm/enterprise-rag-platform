"use client";

import { FileText, LayoutDashboard, MessageSquare, Shield } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";

const links = [
  { href: "/", icon: MessageSquare, label: "Chat" },
  { href: "/documents", icon: FileText, label: "Documents" },
  { href: "/admin", icon: LayoutDashboard, label: "Admin", roles: ["admin", "analyst"] },
];

export function Sidebar({ role }: { role?: string }) {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/50 p-4 flex flex-col gap-2">
      <div className="flex items-center gap-2 px-3 py-4 mb-4">
        <Shield className="w-6 h-6 text-brand-500" />
        <div>
          <h1 className="font-semibold text-sm">Enterprise RAG</h1>
          <p className="text-xs text-slate-400">Internal AI Platform</p>
        </div>
      </div>
      {links.map(({ href, icon: Icon, label, roles }) => {
        if (roles && role && !roles.includes(role)) return null;
        return (
          <Link
            key={href}
            href={href}
            className={clsx(
              "flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors",
              pathname === href
                ? "bg-brand-500/20 text-brand-500"
                : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
            )}
          >
            <Icon className="w-4 h-4" />
            {label}
          </Link>
        );
      })}
    </aside>
  );
}
