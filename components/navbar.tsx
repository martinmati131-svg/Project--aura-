'use client'
import { AnimatedThemeToggler } from '@/components/ui/animated-theme-toggler'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { Menu, X } from 'lucide-react'
import Link from 'next/link'
import React from 'react'

const menuItems = [
  { name: 'Features', href: '#features' },
  { name: 'Team', href: '#team' },
  { name: 'Testimonials', href: '#testimonials' },
  { name: 'Pricing', href: '#pricing' },
  { name: 'FAQ', href: '#faq' },
]

export const Navbar = () => {
  const [menuState, setMenuState] = React.useState(false)
  const [isScrolled, setIsScrolled] = React.useState(false)

  React.useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <nav
      data-state={menuState && 'active'}
      className="fixed z-20 w-full px-2"
    >
      <div className={cn('mx-auto mt-2 max-w-5xl rounded-2xl border bg-background/80 backdrop-blur-md transition-all duration-300', isScrolled && 'shadow-md')}>
        <div className="relative flex flex-col p-3 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex w-full items-center justify-between lg:w-auto">
            <Link
              href="/"
              aria-label="home"
              className="flex items-center gap-2"
            >
              <div className="flex h-6 w-6 items-center justify-center">
                <svg
                  className="h-6 w-6"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
                </svg>
              </div>
              <span className="text-xl font-bold">Aura</span>
            </Link>

            <button
              onClick={() => setMenuState(!menuState)}
              aria-label={menuState ? 'Close Menu' : 'Open Menu'}
              className="relative z-20 block p-2 lg:hidden"
            >
              {menuState ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>

          <div className="hidden lg:flex lg:items-center lg:gap-8">
            <ul className="flex gap-8 text-sm">
              {menuItems.map((item, index) => (
                <li key={index}>
                  <Link
                    href={item.href}
                    className="text-muted-foreground hover:text-foreground transition-colors"
                  >
                    <span>{item.name}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div className="hidden lg:flex lg:items-center lg:gap-4">
            <AnimatedThemeToggler />
            <Button size="sm">Get Started</Button>
          </div>

          {/* Mobile menu */}
          {menuState && (
            <div className="mt-4 flex flex-col gap-4 border-t pt-4 lg:hidden">
              <ul className="space-y-3 text-base">
                {menuItems.map((item, index) => (
                  <li key={index}>
                    <Link
                      href={item.href}
                      onClick={() => setMenuState(false)}
                      className="text-muted-foreground hover:text-foreground block transition-colors"
                    >
                      <span>{item.name}</span>
                    </Link>
                  </li>
                ))}
              </ul>
              <div className="flex items-center justify-between border-t pt-4">
                <AnimatedThemeToggler />
                <Button size="sm">Get Started</Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}

