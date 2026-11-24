export type PostItem = {
  id: string;
  date: string;
  tag: "ROBOTICS" | "EDGE-AI" | "PYTHON" | "RELEASE";
  title: string;
  summary: string;
  href: string;
  external?: boolean;
};

export const AURA_POSTS: PostItem[] = [
  {
    id: "bi-directional-telemetry",
    date: "2026-11-24",
    tag: "ROBOTICS",
    title: "Bi-Directional Serial Command Deck & SSE Bridge",
    summary:
      "Live hardware telemetry streaming over Server-Sent Events with instant E-STOP, zero-point calibration, and stepper motor jog controls.",
    href: "/dashboard",
  },
  {
    id: "manim-visual-explainers",
    date: "2026-11-22",
    tag: "PYTHON",
    title: "Programmatic Technical Animations with Manim",
    summary:
      "Generating crisp mathematical and system-architecture motion graphics directly from Python scripts.",
    href: "https://www.facebook.com/share/v/1E8aUKH8pC/",
    external: true,
  },
  {
    id: "gr00t-edge-pipeline",
    date: "2026-11-18",
    tag: "EDGE-AI",
    title: "Vision-Language-Action Inference & Local Bridge Setup",
    summary:
      "Architecture notes on pairing Raspberry Pi 5 edge nodes with local HTTP/Serial telemetry bridges.",
    href: "/docs",
  },
];
