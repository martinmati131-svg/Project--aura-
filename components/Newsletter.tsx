"use client";

import { useState } from "react";
import { Send, CheckCircle2 } from "lucide-react";

export default function Newsletter() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setSubmitted(true);
      setEmail("");
    }
  };

  return (
    <div className="my-12 p-6 sm:p-8 rounded-2xl bg-muted/40 border text-center max-w-2xl mx-auto">
      <h3 className="text-xl font-bold mb-2">Subscribe to Project Aura</h3>
      <p className="text-sm text-muted-foreground mb-6">
        Get updates on Edge AI, robotics, and high-performance Web development delivered to your inbox.
      </p>

      {submitted ? (
        <div className="flex items-center justify-center gap-2 text-green-500 font-medium text-sm py-2">
          <CheckCircle2 className="h-5 w-5" /> Thanks for subscribing!
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-2 max-w-md mx-auto">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
            className="flex-1 px-4 py-2.5 rounded-xl border bg-background text-sm outline-none focus:ring-2 focus:ring-primary"
          />
          <button
            type="submit"
            className="px-5 py-2.5 rounded-xl bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity flex items-center justify-center gap-2"
          >
            Subscribe <Send className="h-4 w-4" />
          </button>
        </form>
      )}
    </div>
  );
}
