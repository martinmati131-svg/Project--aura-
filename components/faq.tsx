'use client'
import React from 'react'
import { ChevronDown } from 'lucide-react'

const faqs = [
  {
    question: 'What hardware is required to run Project Aura at the edge?',
    answer:
      'Project Aura is designed to run efficiently on low-power devices, mobile environments (like Termux), Raspberry Pis, and edge micro-servers, as well as dedicated GPU infrastructure.',
  },
  {
    question: 'How does custom LoRA fine-tuning work on the platform?',
    answer:
      'You can import your dataset, configure hyper-parameters, and execute adapter training directly. The generated LoRA adapters can then be hot-swapped onto base models without full model retraining.',
  },
  {
    question: 'Can I integrate external vector stores or databases?',
    answer:
      'Yes, Aura supports native connectors for vector databases and local context stores to enable Retrieval-Augmented Generation (RAG) and long-term memory for AI agents.',
  },
  {
    question: 'Is my data secure when executing local workflows?',
    answer:
      'Execution on edge nodes keeps processing localized to your hardware. Data transmitted to the orchestrator is encrypted end-to-end.',
  },
  {
    question: 'How do I upgrade or scale my edge node limits?',
    answer:
      'You can manage and upgrade node allocations directly within your dashboard under workspace settings.',
  },
]

export function FAQ() {
  const [openIndex, setOpenIndex] = React.useState<number | null>(null)

  const toggle = (index: number) => {
    setOpenIndex(openIndex === index ? null : index)
  }

  return (
    <section id="faq" className="py-20 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Frequently Asked Questions
          </h2>
          <p className="mt-4 text-muted-foreground">
            Everything you need to know about setting up and scaling Project Aura.
          </p>
        </div>

        <div className="mx-auto max-w-3xl space-y-4">
          {faqs.map((faq, index) => {
            const isOpen = openIndex === index
            return (
              <div
                key={index}
                className="rounded-2xl border bg-card p-4 transition-all"
              >
                <button
                  onClick={() => toggle(index)}
                  className="flex w-full items-center justify-between text-left font-semibold text-lg"
                  aria-expanded={isOpen}
                >
                  <span>{faq.question}</span>
                  <ChevronDown
                    className={`h-5 w-5 shrink-0 text-muted-foreground transition-transform duration-200 ${
                      isOpen ? 'rotate-180 text-primary' : ''
                    }`}
                  />
                </button>
                {isOpen && (
                  <p className="mt-3 text-sm text-muted-foreground leading-relaxed border-t pt-3">
                    {faq.answer}
                  </p>
                )}
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

export default FAQ
