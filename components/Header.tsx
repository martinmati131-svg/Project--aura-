"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Menu, X, Zap } from "lucide-react";

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="w-full border-b border-border bg-background/95 backdrop-blur">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link 
          href="/" 
          className="flex items-center gap-2 font-bold text-xl tracking-tight"
          aria-label="Aura - Home page"
        >
          <Zap className="h-6 w-6" />
          <span>Aura</span>
        </Link>

        {/* Mobile menu button */}
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className="p-2 rounded-md text-muted-foreground hover:text-foreground md:hidden"
          aria-label={isOpen ? "Close main navigation menu" : "Open main navigation menu"}
          aria-expanded={isOpen}
        >
          {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>
    </header>
  );
}
