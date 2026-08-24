"use client";

import { useChat } from "@ai-sdk/react";
import { useState } from "react";
import { Bot, X, Send } from "lucide-react";

export default function AIChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const { messages, input, handleInputChange, handleSubmit, status } = useChat();

  const isLoading = status === "submitted" || status === "streaming";

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="flex items-center gap-2 bg-primary text-primary-foreground px-4 py-3 rounded-full shadow-lg hover:opacity-90 transition-all font-medium text-sm"
        >
          <Bot className="h-5 w-5" /> Ask Aura AI
        </button>
      ) : (
        <div className="w-80 sm:w-96 h-[450px] bg-background border rounded-2xl shadow-2xl flex flex-col overflow-hidden">
          <div className="flex justify-between items-center p-3.5 border-b bg-muted/50">
            <div className="flex items-center gap-2 font-semibold text-sm">
              <Bot className="h-4 w-4 text-blue-500" /> Aura AI Assistant
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 rounded-md hover:bg-muted text-muted-foreground"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3 text-sm">
            {messages.length === 0 && (
              <p className="text-muted-foreground text-xs text-center mt-8">
                Ask me anything about Project Aura!
              </p>
            )}
            {messages.map((m) => (
              <div
                key={m.id}
                className={`flex gap-2 ${
                  m.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-xl px-3 py-2 text-xs sm:text-sm ${
                    m.role === "user"
                      ? "bg-blue-600 text-white"
                      : "bg-muted text-foreground border"
                  }`}
                >
                  {m.content}
                </div>
              </div>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="p-3 border-t flex gap-2">
            <input
              value={input}
              onChange={handleInputChange}
              placeholder="Ask a question..."
              className="flex-1 bg-muted px-3 py-1.5 rounded-lg text-xs outline-none focus:ring-1 focus:ring-primary"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="p-2 bg-primary text-primary-foreground rounded-lg disabled:opacity-50"
            >
              <Send className="h-3.5 w-3.5" />
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
