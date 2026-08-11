'use client'
import { Cpu, Zap, ShieldCheck, Workflow, Database, Sliders } from 'lucide-react'

const features = [
  {
    icon: Cpu,
    title: 'Edge AI Deployment',
    description: 'Run lightweight, low-latency models directly on edge hardware and local environments.',
  },
  {
    icon: Sliders,
    title: 'Fine-Tuning & LoRA',
    description: 'Seamlessly integrate custom LoRA adapters and fine-tune models on domain-specific datasets.',
  },
  {
    icon: Workflow,
    title: 'Autonomous Workflows',
    description: 'Orchestrate multi-step AI agents and task pipelines with automated decision loops.',
  },
  {
    icon: Zap,
    title: 'High-Performance Inference',
    description: 'Optimized execution pipelines designed for real-time response and resource efficiency.',
  },
  {
    icon: Database,
    title: 'Vector & Context Store',
    description: 'Connect external knowledge bases and long-term memory structures effortlessly.',
  },
  {
    icon: ShieldCheck,
    title: 'Enterprise Security',
    description: 'End-to-end encrypted communication and localized execution control.',
  },
]

export function Features() {
  return (
    <section id="features" className="py-20 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Engineered for Next-Gen Intelligence
          </h2>
          <p className="mt-4 text-muted-foreground">
            Everything you need to build, fine-tune, and deploy autonomous AI systems.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <div
                key={index}
                className="rounded-2xl border bg-card p-6 shadow-sm transition-all hover:shadow-md"
              >
                <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <Icon className="h-5 w-5" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

export default Features
