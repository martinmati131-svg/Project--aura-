import ShareButtons from "./ShareButtons";
import { calculateReadingTime } from "@/lib/readingTime";
import { Clock, Calendar } from "lucide-react";

interface BlogPostProps {
  title: string;
  date: string;
  slug: string;
  content: string;
  children: React.ReactNode;
}

export default function BlogPost({ title, date, slug, content, children }: BlogPostProps) {
  const { text: readTime } = calculateReadingTime(content);

  return (
    <article className="max-w-3xl mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-4">{title}</h1>
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span className="flex items-center gap-1">
            <Calendar className="h-4 w-4" /> {date}
          </span>
          <span className="flex items-center gap-1">
            <Clock className="h-4 w-4" /> {readTime}
          </span>
        </div>
        <ShareButtons title={title} slug={slug} />
      </header>
      <div className="prose dark:prose-invert max-w-none">{children}</div>
    </article>
  );
}
