"use client";

import { useState } from "react";
import Fuse from "fuse.js";

interface Post {
  id: string;
  title: string;
  summary: string;
  slug: string;
}

interface SearchBarProps {
  posts: Post[];
  onSearch: (results: Post[]) => void;
}

export default function SearchBar({ posts, onSearch }: SearchBarProps) {
  const [query, setQuery] = useState("");

  const fuse = new Fuse(posts, {
    keys: ["title", "summary"],
    threshold: 0.3,
  });

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);

    if (!value.trim()) {
      onSearch(posts);
      return;
    }

    const results = fuse.search(value).map((result) => result.item);
    onSearch(results);
  };

  return (
    <div className="w-full mb-6">
      <input
        type="text"
        value={query}
        onChange={handleSearch}
        placeholder="Search posts..."
        className="w-full px-4 py-2 border rounded-lg bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
  );
}
