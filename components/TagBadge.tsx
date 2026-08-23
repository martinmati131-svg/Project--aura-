import Link from "next/link";

interface TagBadgeProps {
  tag: string;
}

export default function TagBadge({ tag }: TagBadgeProps) {
  return (
    <Link
      href={`/tags/${encodeURIComponent(tag.toLowerCase())}`}
      className="inline-block px-2.5 py-1 text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300 rounded-full hover:bg-blue-200 transition-colors"
    >
      #{tag}
    </Link>
  );
}
