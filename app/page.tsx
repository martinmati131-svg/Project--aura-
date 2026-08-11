import { Navbar } from '@/components/navbar'
import HeroSection from '@/components/hero-section'
import Features from '@/components/features'
import Pricing from '@/components/pricing'
import FAQ from '@/components/faq'
import Footer from '@/components/footer'

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      <HeroSection />
      <Features />
      <Pricing />
      <FAQ />
      <Footer />
    </main>
  )
}
