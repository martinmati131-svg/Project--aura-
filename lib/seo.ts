import { Metadata } from "next";

export function constructMetadata({
  title = "Project Aura - Edge AI & Robotics Platform",
  description = "Open-source Edge AI, autonomous robotics, and modern web software documentation.",
  image = "/og-image.png",
  icons = "/favicon.ico",
}: {
  title?: string;
  description?: string;
  image?: string;
  icons?: string;
} = {}): Metadata {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://project-aura.vercel.app";

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      url: siteUrl,
      siteName: "Project Aura",
      images: [{ url: `${siteUrl}${image}` }],
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [`${siteUrl}${image}`],
      creator: "@aura_ai",
    },
    icons,
    metadataBase: new URL(siteUrl),
  };
}
