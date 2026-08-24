"use client";

import React from "react";

export default function TeamSection() {
  const team = [
    {
      name: "Martin Mati",
      role: "Lead Architect & Founder",
      bio: "Building Edge AI, robotics infrastructure, and intelligent applications.",
    },
  ];

  return (
    <section className="py-12 bg-background border-t">
      <div className="max-w-4xl mx-auto px-4">
        <h2 className="text-2xl font-bold tracking-tight mb-6">Team</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {team.map((member, idx) => (
            <div key={idx} className="p-6 border rounded-xl bg-card">
              <h3 className="font-semibold text-lg">{member.name}</h3>
              <p className="text-xs text-muted-foreground mb-2">{member.role}</p>
              <p className="text-sm text-muted-foreground">{member.bio}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
