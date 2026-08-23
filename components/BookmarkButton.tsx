"use client";

import { useState, useEffect } from "react";
import { Bookmark } from "lucide-react";

interface BookmarkButtonProps {
  postId: string;
}

export default function BookmarkButton({ postId }: BookmarkButtonProps) {
  const [isBookmarked, setIsBookmarked] = useState(false);

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem("bookmarked_posts") || "[]");
    setIsBookmarked(saved.includes(postId));
  }, [postId]);

  const toggleBookmark = () => {
    const saved: string[] = JSON.parse(
      localStorage.getItem("bookmarked_posts") || "[]"
    );
    let updated: string[];

    if (saved.includes(postId)) {
      updated = saved.filter((id) => id !== postId);
    } else {
      updated = [...saved, postId];
    }

    localStorage.setItem("bookmarked_posts", JSON.stringify(updated));
    setIsBookmarked(!isBookmarked);
  };

  return (
    <button
      onClick={toggleBookmark}
      className={`p-2 rounded-lg border transition-colors flex items-center gap-2 text-sm font-medium ${
        isBookmarked
          ? "bg-blue-600 text-white border-blue-600"
          : "bg-background hover:bg-muted border-border"
      }`}
    >
      <Bookmark className={`w-4 h-4 ${isBookmarked ? "fill-current" : ""}`} />
      {isBookmarked ? "Saved" : "Save for later"}
    </button>
  );
}
