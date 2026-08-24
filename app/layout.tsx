import { ThemeProvider } from "@/components/ThemeProvider";
import ThemeToggle from "@/components/ThemeToggle";
import { SpeedInsights } from "@vercel/speed-insights/next";
import "./globals.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-background text-foreground antialiased">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <header className="flex justify-between items-center p-4 max-w-4xl mx-auto border-b">
            <h1 className="font-bold text-lg">Project Aura</h1>
            <ThemeToggle />
          </header>
          {children}
          <SpeedInsights />
        </ThemeProvider>
      </body>
    </html>
  );
}
