"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AURA_POSTS, type PostItem } from "../data/posts";

const TAGS = ["ALL", "ROBOTICS", "EDGE-AI", "PYTHON", "RELEASE"] as const;

export default function HomePage() {
  const [posts, setPosts] = useState<PostItem[]>(AURA_POSTS);
  useEffect(() => {
    try {
      const raw = window.localStorage.getItem("aura_custom_posts_v1");
      if (!raw) return;
      const saved: PostItem[] = JSON.parse(raw);
      if (Array.isArray(saved) && saved.length > 0) {
        setPosts((prev) => {
          const existingIds = new Set(prev.map((item) => item.id));
          const uniqueSaved = saved.filter((item) => item && !existingIds.has(item.id));
          return [...uniqueSaved, ...prev];
        });
      }
    } catch {
      // Ignore storage read/parse errors
    }
  }, []);
  const [activeTag, setActiveTag] = useState<(typeof TAGS)[number]>("ALL");
  const [showComposer, setShowComposer] = useState(false);
  const [title, setTitle] = useState("");
  const [summary, setSummary] = useState("");
  const [tag, setTag] = useState<PostItem["tag"]>("ROBOTICS");
  const [href, setHref] = useState("/dashboard");

  const visiblePosts =
    activeTag === "ALL" ? posts : posts.filter((p) => p.tag === activeTag);

  function handleAddPost(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || !summary.trim()) return;

    const newPost: PostItem = {
      id: `post-${Date.now()}`,
      date: new Date().toISOString().slice(0, 10),
      tag,
      title: title.trim(),
      summary: summary.trim(),
      href: href.trim() || "/docs",
      external: href.trim().startsWith("http"),
    };

    const updated = [newPost, ...posts];
    setPosts(updated);
    try {
      const seedIds = new Set(AURA_POSTS.map((item) => item.id));
      const customOnly = updated.filter((item) => !seedIds.has(item.id));
      window.localStorage.setItem("aura_custom_posts_v1", JSON.stringify(customOnly));
    } catch {
      // Ignore storage write errors
    }
    setTitle("");
    setSummary("");
    setHref("/dashboard");
    setShowComposer(false);
  }

  return (
    <main className="mx-auto min-h-screen max-w-5xl px-6 py-12">
      {/* Top Navigation */}
      <header className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-2.5">
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />
          <span className="font-mono text-sm font-bold tracking-wider text-white">
            AURA INTELLIGENCE
          </span>
        </div>
        <nav className="flex items-center gap-5 font-mono text-xs text-slate-300">
          <Link href="/" className="text-sky-400">
            HOME
          </Link>
          <Link href="/dashboard" className="text-cyan-400 hover:text-cyan-300 font-semibold">
            TELEMETRY
          </Link>
          <Link href="/docs" className="hover:text-white">
            DOCS
          </Link>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="py-12">
        <span className="rounded-full border border-sky-500/30 bg-sky-500/10 px-3 py-1 font-mono text-xs text-sky-300">
          EDGE-AI &amp; EMBODIED ROBOTICS
        </span>
        <h1 className="mt-4 text-3xl font-bold tracking-tight text-white sm:text-5xl">
          Real-Time Hardware Telemetry &amp; Control Deck
        </h1>
        <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate-300">
          Stream live sensor packets from edge nodes, dispatch bi-directional
          serial actuator commands, and publish engineering updates from one
          unified workspace.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            href="/dashboard"
            className="rounded-lg bg-sky-600 px-5 py-2.5 font-mono text-xs font-semibold text-white transition hover:bg-sky-500"
          >
            OPEN TELEMETRY CONSOLE →
          </Link>
          <Link
            href="/docs"
            className="rounded-lg border border-slate-700 bg-slate-900 px-5 py-2.5 font-mono text-xs font-semibold text-slate-200 transition hover:border-slate-500"
          >
            READ ARCHITECTURE DOCS
          </Link>
        </div>
      </section>

      {/* Posts / Engineering Log Section */}
      <section className="border-t border-slate-800 pt-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-semibold text-white">
              Engineering Logs &amp; Posts
            </h2>
            <p className="mt-1 text-sm text-slate-400">
              Field notes, robotics telemetry updates, and Python/Manim demos.
            </p>
          </div>
          <button
            type="button"
            onClick={() => setShowComposer((v) => !v)}
            className="rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-3.5 py-2 font-mono text-xs font-semibold text-emerald-300 transition hover:bg-emerald-500/20"
          >
            {showComposer ? "CLOSE COMPOSER" : "+ NEW POST"}
          </button>
        </div>

        {/* Quick Post Composer */}
        {showComposer && (
          <form
            onSubmit={handleAddPost}
            className="mt-6 space-y-4 rounded-xl border border-slate-800 bg-slate-900/70 p-5"
          >
            <div className="grid gap-4 sm:grid-cols-3">
              <input
                type="text"
                placeholder="Post title..."
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white placeholder-slate-500 focus:border-sky-500 focus:outline-none sm:col-span-2"
                required
              />
              <select
                value={tag}
                onChange={(e) => setTag(e.target.value as PostItem["tag"])}
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-xs text-slate-200 focus:border-sky-500 focus:outline-none"
              >
                <option value="ROBOTICS">ROBOTICS</option>
                <option value="EDGE-AI">EDGE-AI</option>
                <option value="PYTHON">PYTHON</option>
                <option value="RELEASE">RELEASE</option>
              </select>
            </div>
            <textarea
              rows={2}
              placeholder="Write a short summary or field note..."
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white placeholder-slate-500 focus:border-sky-500 focus:outline-none"
              required
            />
            <div className="flex flex-wrap items-center justify-between gap-3">
              <input
                type="text"
                placeholder="Link (/dashboard, /docs, or https://...)"
                value={href}
                onChange={(e) => setHref(e.target.value)}
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-xs text-slate-200 placeholder-slate-500 focus:border-sky-500 focus:outline-none sm:w-80"
              />
              <button
                type="submit"
                className="rounded-lg bg-emerald-600 px-4 py-2 font-mono text-xs font-semibold text-white transition hover:bg-emerald-500"
              >
                PUBLISH TO FEED
              </button>
            </div>
          </form>
        )}

        {/* Tag Filter Bar */}
        <div className="mt-6 flex flex-wrap gap-2">
          {TAGS.map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => setActiveTag(t)}
              className={`rounded-full px-3 py-1 font-mono text-xs transition ${
                activeTag === t
                  ? "bg-sky-600 text-white"
                  : "border border-slate-800 bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {/* Post Cards Grid */}
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {visiblePosts.map((post) => (
            <article
              key={post.id}
              className="flex flex-col justify-between rounded-xl border border-slate-800 bg-slate-900/50 p-5 transition hover:border-slate-700"
            >
              <div>
                <div className="flex items-center justify-between gap-2 font-mono text-xs">
                  <span className="rounded bg-sky-500/10 px-2 py-0.5 text-sky-300">
                    {post.tag}
                  </span>
                  <span className="text-slate-500">{post.date}</span>
                </div>
                <h3 className="mt-3 text-base font-semibold text-white">
                  {post.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-300">
                  {post.summary}
                </p>
              </div>
              <div className="mt-5">
                <Link
                  href={post.href}
                  target={post.external ? "_blank" : undefined}
                  rel={post.external ? "noopener noreferrer" : undefined}
                  className="font-mono text-xs font-semibold text-sky-400 hover:text-sky-300"
                >
                  {post.external ? "OPEN EXTERNAL LINK ↗" : "VIEW DETAILS →"}
                </Link>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
