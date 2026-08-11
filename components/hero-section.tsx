'use client'
import { Button } from '@/components/ui/button'

export function HeroSection() {
  return (
    <section className="relative overflow-hidden pt-32 pb-16 md:pt-40 md:pb-24">
      <div className="container mx-auto px-4 text-center">
        <div className="mx-auto mb-6 inline-flex items-center gap-2 rounded-full border bg-background/50 px-4 py-1.5 text-sm font-medium backdrop-blur-sm">
          <span>Introducing Project Aura ✨</span>
        </div>

        <h1 className="mx-auto max-w-4xl text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
          Next-Gen AI Platform for Autonomous Workflows
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground md:text-xl">
          Build, train, and deploy intelligent AI agents and edge workflows effortlessly.
        </p>

        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <Button size="lg" className="rounded-full px-8">
            Get Started Free
          </Button>
          <Button size="lg" variant="outline" className="rounded-full px-8">
            Documentation
          </Button>
        </div>
      </div>
    </section>
  )
}

export default HeroSection
