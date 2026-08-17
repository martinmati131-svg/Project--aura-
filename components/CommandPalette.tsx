cat << 'EOF' > components/CommandPalette.tsx
"use client";

import React, { useEffect, useState } from "react";
import { Command } from "cmdk";
import { Search, Rocket, BarChart2, BookOpen, Terminal } from "lucide-react";

export function CommandPalette() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <Command className="w-full max-w-xl bg-zinc-900 border border-zinc-800 rounded-xl shadow-2xl overflow-hidden text-zinc-100">
        <div className="flex items-center border-b border-zinc-800 px-3">
          <Search className="w-4 h-4 text-zinc-400 mr-2" />
          <Command.Input
            placeholder="Type a command or search..."
            className="w-full bg-transparent py-3 text-sm outline-none placeholder:text-zinc-500"
          />
        </div>
        <Command.List className="max-h-80 overflow-y-auto p-2 space-y-1">
          <Command.Empty className="p-4 text-xs text-zinc-500 text-center">
            No results found.
          </Command.Empty>

          <Command.Group heading="Navigation" className="text-xs text-zinc-500 px-2 py-1 font-semibold">
            <Command.Item
              onSelect={() => { window.location.href = "#"; setOpen(false); }}
              className="flex items-center gap-2 px-3 py-2 text-sm rounded-md cursor-pointer hover:bg-zinc-800 aria-selected:bg-zinc-800"
            >
              <Rocket className="w-4 h-4 text-emerald-400" />
              <span>Overview</span>
            </Command.Item>
            <Command.Item
              onSelect={() => { window.location.href = "#analytics"; setOpen(false); }}
              className="flex items-center gap-2 px-3 py-2 text-sm rounded-md cursor-pointer hover:bg-zinc-800 aria-selected:bg-zinc-800"
            >
              <BarChart2 className="w-4 h-4 text-blue-400" />
              <span>Telemetry & Analytics</span>
            </Command.Item>
            <Command.Item
              onSelect={() => { window.location.href = "#docs"; setOpen(false); }}
              className="flex items-center gap-2 px-3 py-2 text-sm rounded-md cursor-pointer hover:bg-zinc-800 aria-selected:bg-zinc-800"
            >
              <BookOpen className="w-4 h-4 text-purple-400" />
              <span>Documentation</span>
            </Command.Item>
          </Command.Group>

          <Command.Group heading="Actions" className="text-xs text-zinc-500 px-2 py-1 font-semibold mt-2">
            <Command.Item
              onSelect={() => { window.open("https://github.com/martinmati131-svg/Project--aura-", "_blank"); setOpen(false); }}
              className="flex items-center gap-2 px-3 py-2 text-sm rounded-md cursor-pointer hover:bg-zinc-800 aria-selected:bg-zinc-800"
            >
              <Terminal className="w-4 h-4 text-amber-400" />
              <span>Open GitHub Repository</span>
            </Command.Item>
          </Command.Group>
        </Command.List>
      </Command>
    </div>
  );
}
EOF
