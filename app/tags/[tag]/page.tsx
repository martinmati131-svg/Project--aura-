import Link from "next/link";

interface TagPageProps {
  params: Promise<{ tag: string }>;
}

export default async function TagPage({ params }: TagPageProps) {
  const { tag } = await params;
  const decodedTag = decodeURIComponent(tag);

  return (
    <main className="max-w-4xl mx-auto px-4 py-10">
      <div className="mb-8">
        <Link 
          href="/" 
          className="text-sm text-blue-500 hover:underline mb-2 inline-block"
        >
          ← Back to all posts
        </Link>
        <h1 className="text-3xl font-bold tracking-tight">
          Posts tagged with <span className="text-blue-600">#{decodedTag}</span>
        </h1>
      </div>

      <div className="p-6 border rounded-xl bg-card">
        <p className="text-muted-foreground">
          Showing articles categorized under #{decodedTag}.
        </p>
      </div>
    </main>
  );
}
