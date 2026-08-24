export function calculateReadingTime(content: string): { text: string; minutes: number; words: number } {
  const wordsPerMinute = 200;
  const words = content.trim().split(/\s+/).length;
  const minutes = Math.ceil(words / wordsPerMinute);
  return {
    text: `${minutes} min read`,
    minutes,
    words,
  };
}
