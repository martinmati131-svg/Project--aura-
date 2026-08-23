import RSS from "rss";

export async function GET() {
  const feed = new RSS({
    title: "Project Aura",
    description: "Latest insights, tech notes, and updates from Project Aura.",
    site_url: "https://project-aura.vercel.app",
    feed_url: "https://project-aura.vercel.app/feed.xml",
    copyright: `${new Date().getFullYear()} Project Aura`,
    language: "en",
  });

  // Example item structure — replace with your dynamic post fetcher if needed
  feed.item({
    title: "Welcome to Project Aura",
    description: "An overview of the Project Aura architecture and feature roadmap.",
    url: "https://project-aura.vercel.app/posts/welcome",
    date: new Date(),
  });

  return new Response(feed.xml({ indent: true }), {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
    },
  });
}
