'use client'
import { Button } from '@/components/ui/button'
import { Check } from 'lucide-react'

const plans = [
  {
    name: 'Starter',
    price: '$0',
    description: 'Perfect for prototyping edge models and personal experiments.',
    features: [
      'Single edge-node deployment',
      'Basic model fine-tuning',
      'Community support',
      '1GB vector storage',
    ],
    buttonText: 'Get Started Free',
    popular: false,
  },
  {
    name: 'Pro Developer',
    price: '$29',
    period: '/month',
    description: 'For power developers fine-tuning LoRA adapters and automated workflows.',
    features: [
      'Up to 10 edge nodes',
      'Custom LoRA adapter fine-tuning',
      'Autonomous agent execution loops',
      'Priority inference queue',
      '10GB vector storage',
    ],
    buttonText: 'Start Pro Trial',
    popular: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    description: 'Dedicated infrastructure, custom model integration, and SLA support.',
    features: [
      'Unlimited edge nodes',
      'Dedicated training cluster',
      'Custom model architectures',
      '24/7 dedicated support',
      'Unlimited vector storage',
    ],
    buttonText: 'Contact Sales',
    popular: false,
  },
]

export function Pricing() {
  return (
    <section id="pricing" className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Flexible Plans for Every Developer
          </h2>
          <p className="mt-4 text-muted-foreground">
            Scale your edge AI capabilities and autonomous workflows seamlessly.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`relative flex flex-col justify-between rounded-2xl border p-6 shadow-sm transition-all ${
                plan.popular ? 'border-primary shadow-md bg-card' : 'bg-card/50'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-primary px-3 py-1 text-xs font-semibold text-primary-foreground">
                  Most Popular
                </div>
              )}
              <div>
                <h3 className="text-xl font-bold">{plan.name}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{plan.description}</p>
                <div className="mt-6 flex items-baseline">
                  <span className="text-4xl font-extrabold tracking-tight">{plan.price}</span>
                  {plan.period && (
                    <span className="ml-1 text-sm text-muted-foreground">{plan.period}</span>
                  )}
                </div>
                <ul className="mt-6 space-y-3">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center gap-3 text-sm">
                      <Check className="h-4 w-4 text-primary shrink-0" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="mt-8">
                <Button
                  className="w-full rounded-full"
                  variant={plan.popular ? 'default' : 'outline'}
                >
                  {plan.buttonText}
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Pricing
