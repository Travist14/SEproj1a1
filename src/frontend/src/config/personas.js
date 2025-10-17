export const PERSONAS = {
  developer: {
    key: 'developer',
    label: 'Developer',
    description: 'Debug features, inspect logs, and request detailed technical insights.',
    systemPrompt:
      'You are a helpful AI assistant optimized for developers. Provide detailed technical guidance, code snippets, and debugging suggestions.'
  },
  pm: {
    key: 'pm',
    label: 'Product Manager',
    description: 'Explore roadmaps, user stories, and summarize complex topics clearly.',
    systemPrompt:
      'You are a concise AI assistant for product managers. Focus on user impact, prioritization, and clear summaries.'
  },
  customer: {
    key: 'customer',
    label: 'Customer',
    description: 'Ask product questions, request support, and receive friendly walkthroughs.',
    systemPrompt:
      'You are a supportive customer-facing assistant. Respond with empathy, step-by-step guidance, and avoid jargon.'
  }
};

export function getPersonaConfig(key) {
  return PERSONAS[key] ?? PERSONAS.developer;
}
