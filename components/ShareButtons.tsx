"use client";

import { useState } from "react";
import { Share2, Link as LinkIcon, Check, Twitter, Linkedin } from "lucide-react";

interface ShareProps {
  title: string;
  slug: string;
}

export default function ShareButtons({ title, slug }: ShareProps) {
  const [copied, setCopied] = useState(false);
  const shareUrl = typeof window !== "undefined" ? `${window.location.origin}/blog/${slug}` : "";

  const copyToClipboard = async () => {
    if (!shareUrl) return;
    await navigator.clipboard.writeText(shareUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(shareUrl)}`;
  const linkedinUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`;

  return (
    <div className="flex items-center gap-2 py-4 border-y my-6">
      <span className="text-xs font-medium text-muted-foreground flex items-center gap-1 mr-2">
        <Share2 className="h-3.5 w-3.5" /> Share
      </span>
      <a
        href={twitterUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="p-2 rounded-full bg-muted hover:bg-accent transition-colors"
        aria-label="Share on X"
      >
        <Twitter className="h-4 w-4" />
      </a>
      <a
        href={linkedinUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="p-2 rounded-full bg-muted hover:bg-accent transition-colors"
        aria-label="Share on LinkedIn"
      >
        <Linkedin className="h-4 w-4" />
      </a>
      <button
        onClick={copyToClipboard}
        className="p-2 rounded-full bg-muted hover:bg-accent transition-colors"
        aria-label="Copy link"
      >
        {copied ? <Check className="h-4 w-4 text-green-500" /> : <LinkIcon className="h-4 w-4" />}
      </button>
    </div>
  );
}
