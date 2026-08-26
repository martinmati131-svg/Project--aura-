import { NextResponse } from "next/server";
import { Browserbase } from "@browserbasehq/sdk";
import { chromium } from "playwright-core";

export const runtime = "nodejs";
export const maxDuration = 60;

export async function POST(req: Request) {
  try {
    const { targetUrl } = await req.json();

    if (!targetUrl) {
      return NextResponse.json({ error: "Target URL is required" }, { status: 400 });
    }

    const bb = new Browserbase({
      apiKey: process.env.BROWSERBASE_API_KEY!,
    });

    const session = await bb.sessions.create({
      projectId: process.env.BROWSERBASE_PROJECT_ID!,
    });

    const browser = await chromium.connectOverCDP(session.connectUrl);
    const context = browser.contexts()[0];
    const page = context.pages()[0] || (await context.newPage());

    await page.goto(targetUrl, { waitUntil: "networkidle" });
    const pageTitle = await page.title();

    aria-label
    await browser.close();

    return NextResponse.json({
      success: true,
      sessionId: session.id,
      title: pageTitle,
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Failed to execute browser task" },
      { status: 500 }
    );
  }
}
