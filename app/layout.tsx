import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://powerdreams.top"),
  title: {
    default: "Aura Intelligence | Open-Source Edge AI & Robotics",
    template: "%s | Aura Intelligence",
  },
  description: "Open-source Edge AI architectures, ROS 2 hardware integration, and intelligent system deployments.",
  openGraph: {
    title: "Aura Intelligence | Open-Source Edge AI & Robotics",
    description: "Open-source Edge AI architectures, ROS 2 hardware integration, and intelligent system deployments.",
    url: "https://powerdreams.top",
    siteName: "Aura Intelligence",
    images: [
      {
        url: "https://blogger.googleusercontent.com/img/a/AVvXsEjKb2hR1wH13VmM1he3BdUDdYWxcJXgH5XzbxDoG7crnkFnaruZvEoSr80C_8yyWUe3GbYDwJF2kp1LqyW40ILuJeN-NSflPmbk4NXPdf9YfQ9L35C2_bbQ-JhNzsxb3CsVIKdQaGVbYbVpNfD6tZGTylVd_LFYvEtCeoof4ZlxK_0iyh4SLsOUrYNr19nl=w1200-h630-p-k-no-nu",
        width: 1024,
        height: 559,
        alt: "Aura Intelligence Hardware Setup",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Aura Intelligence | Open-Source Edge AI & Robotics",
    description: "Open-source Edge AI architectures, ROS 2 hardware integration, and intelligent system deployments.",
    images: ["https://blogger.googleusercontent.com/img/a/AVvXsEjKb2hR1wH13VmM1he3BdUDdYWxcJXgH5XzbxDoG7crnkFnaruZvEoSr80C_8yyWUe3GbYDwJF2kp1LqyW40ILuJeN-NSflPmbk4NXPdf9YfQ9L35C2_bbQ-JhNzsxb3CsVIKdQaGVbYbVpNfD6tZGTylVd_LFYvEtCeoof4ZlxK_0iyh4SLsOUrYNr19nl=w1200-h630-p-k-no-nu"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-background text-foreground">
        {children}
      </body>
    </html>
  );
}
