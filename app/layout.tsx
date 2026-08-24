import { ThemeProvider } from "@/components/ThemeProvider";
import ThemeToggle from "@/components/ThemeToggle";
import CommandPalette from "@/components/CommandPalette";
import ScrollProgress from "@/components/ScrollProgress";
import { SpeedInsights } from "@vercel/speed-insights/next";
import "./globals.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-background text-foreground antialiased min-h-screen">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <ScrollProgress />
          <CommandPalette />
          <header className="flex justify-between items-center p-4 max-w-4xl mx-auto border-b">
            <h1 className="font-bold text-lg">Project Aura</h1>
            <div className="flex items-center gap-2">
              <span className="text-xs text-muted-foreground hidden sm:inline-block">
                Press <kbd className="px-1.5 py-0.5 text-xs bg-muted border rounded">⌘K</kbd>
              </span>
              <ThemeToggle />
            </div>
          </header>
          {children}
          <SpeedInsights />
        </ThemeProvider>
      </body>
    </html>
  );
}
