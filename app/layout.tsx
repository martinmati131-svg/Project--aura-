import type { Metadata } from "next";

export const metadata: Metadata = {
  metadataBase: new URL("https://powerdreams.top"),
  title: {
    default: "Project Aura | Open-Source Edge AI & Robotics",
    template: "%s | Project Aura",
  },
  description: "Building next-generation open-source Edge AI architectures, robotics tools, and web deployments.",
  openGraph: {
    title: "Project Aura",
    description: "Open-source Edge AI & Robotics Infrastructure",
    url: "https://powerdreams.top",
    siteName: "Project Aura",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Project Aura Preview",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Project Aura",
    description: "Open-source Edge AI & Robotics Infrastructure",
    images: ["/og-image.png"],
  },
};
