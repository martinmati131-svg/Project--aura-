import { openai } from "@ai-sdk/openai";
import { streamText } from "ai";

export const runtime = "nodejs";
export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: openai("gpt-4o-mini"),
    system: "You are the AI assistant for Project Aura, an open-source platform focusing on Edge AI, robotics, and Next.js technology. Provide clear, concise, and helpful answers.",
    messages,
  });

  return result.toDataStreamResponse();
}
