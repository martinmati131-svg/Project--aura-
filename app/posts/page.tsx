import { supabase } from "@/lib/supabase";

export const revalidate = 60;

export default async function PostsPage() {
  const { data: posts, error } = await supabase
    .from("posts")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    return <div className="p-4 text-red-500">Failed to load posts.</div>;
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-6">Latest Updates</h1>
      <div className="space-y-4">
        {posts?.map((post) => (
          <article key={post.id} className="p-6 border rounded-lg bg-card">
            <h2 className="text-xl font-semibold">{post.title}</h2>
            <p className="mt-2 text-muted-foreground">{post.content}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
