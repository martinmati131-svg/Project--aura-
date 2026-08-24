import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://project-aura.vercel.app';

  // Sample dynamic routes (replace or expand with MDX/CMS fetch)
  const posts = ['getting-started-with-aura', 'edge-ai-robotics-guide'];

  const blogRoutes = posts.map((slug) => ({
    url: `${baseUrl}/blog/${slug}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1.0,
    },
    ...blogRoutes,
  ];
}
