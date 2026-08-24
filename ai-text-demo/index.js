import 'dotenv/config';
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

async function main() {
  if (!process.env.OPENAI_API_KEY) {
    console.error("Error: OPENAI_API_KEY is not set in environment or .env file.");
    process.exit(1);
  }

  console.log("Connecting to OpenAI API...");

  try {
    const result = streamText({
      model: openai('gpt-4o-mini'),
      prompt: 'Invent a new holiday and describe its traditions in 3 bullet points.',
    });

    for await (const textPart of result.textStream) {
      process.stdout.write(textPart);
    }

    console.log('\n\n--- Done ---');
    const usage = await result.usage;
    console.log('Token usage:', usage);
  } catch (err) {
    console.error("\nExecution Error:", err.message || err);
  }
}

main();
