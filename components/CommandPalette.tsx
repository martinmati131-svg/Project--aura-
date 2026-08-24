"use client";

import * as React from "react";
import { Command } from "cmdk";
import { Search, Moon, Sun, Home } from "lucide-react";
import { useTheme } from "next-themes";
import { useRouter } from "next/navigation";

export default function CommandPalette() {
  const [open, setOpen] = React.useState(false);
  const { setTheme } = useTheme();
  const router = useRouter();

  React.useEffect(() => {
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
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
      <Command className="w-full max-w-lg bg-background border rounded-xl shadow-2xl overflow-hidden p-2">
        <div className="flex items-center border-b px-3">
          <Search className="mr-2 h-4 w-4 shrink-0 opacity-50" />
          <Command.Input
            placeholder="Type a command or search..."
            className="flex h-11 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground"
          />
        </div>
        <Command.List className="max-h-[300px] overflow-y-auto p-2">
          <Command.Empty className="py-6 text-center text-sm text-muted-foreground">
            No results found.
          </Command.Empty>
          <Command.Group heading="Navigation" className="text-xs text-muted-foreground px-2 py-1">
            <Command.Item
              onSelect={() => { router.push("/"); setOpen(false); }}
              className="flex items-center gap-2 px-2 py-1.5 text-sm rounded cursor-pointer hover:bg-accent"
            >
              <Home className="h-4 w-4" /> Home
            </Command.Item>
          </Command.Group>
          <Command.Group heading="Theme" className="text-xs text-muted-foreground px-2 py-1 mt-2">
            <Command.Item
              onSelect={() => { setTheme("light"); setOpen(false); }}
              className="flex items-center gap-2 px-2 py-1.5 text-sm rounded cursor-pointer hover:bg-accent"
            >
              <Sun className="h-4 w-4" /> Light Mode
            </Command.Item>
            <Command.Item
              onSelect={() => { setTheme("dark"); setOpen(false); }}
              className="flex items-center gap-2 px-2 py-1.5 text-sm rounded cursor-pointer hover:bg-accent"
            >
              <Moon className="h-4 w-4" /> Dark Mode
            </Command.Item>
          </Command.Group>
        </Command.List>
      </Command>
    </div>
  );
}
