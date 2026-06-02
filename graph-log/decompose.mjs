// On-demand decomposition. There is NO server-side graph algorithm — the LLM
// produces the prerequisite graph by following the prompt below, then it is
// logged. This module is (1) the prompt the LLM follows, (2) the Kepler worked
// example baked in so the LLM imitates the depth/descent/stopping point, and
// (3) a decompose() that calls a real LLM when one is supplied, or returns the
// baked example offline for the demo.

export const DECOMPOSITION_PROMPT = `You decompose a physics/science TOPIC into its prerequisite graph for an
18-year-old secondary student. Break it down layer by layer into the concepts it
depends on, descending from the subject topic into the underlying math. For each
node, justify why it needs the one beneath it. STOP at the plausibly-missing
floor: equation/variable literacy ("a symbol stands for a number, and = means
both sides are equal"). DO NOT decompose below that (never "what is a number",
counting, etc.).

Worked example — Topic: "Kepler's third law" (T squared is proportional to r cubed):
- Layer 1: proportionality ("is proportional to"); powers/exponents (squared, cubed); ratio (T²/r³ = constant)
- Layer 2: proportionality needs division + the idea of a constant; powers need multiplication; ratio needs division
- Layer 3: division needs multiplication + the equals sign as balance (both sides stay equal); multiplication needs addition
- Layer 4 (FLOOR): addition and the equals sign bottom out at equation/variable literacy — STOP here.

Apply this SAME pattern to any topic you are given.

Return ONLY JSON of this shape:
{
  "topic": "<the topic>",
  "nodes": [{"concept": "<name>", "layer": <int, 0=the topic>, "is_floor": <bool>}],
  "edges": [{"concept": "<name>", "requires": "<prerequisite name>", "why": "<one line>"}]
}`;

// The Kepler decomposition as data — the exact graph the prompt above yields.
// Used offline by the demo as the stand-in for the LLM's output.
export const KEPLER = {
  topic: "Kepler's third law",
  nodes: [
    { concept: "Kepler's third law", layer: 0 },
    { concept: "proportionality", layer: 1 },
    { concept: "powers/exponents", layer: 1 },
    { concept: "ratio", layer: 1 },
    { concept: "division", layer: 2 },
    { concept: "constant", layer: 2 },
    { concept: "multiplication", layer: 2 },
    { concept: "equals sign as balance", layer: 3 },
    { concept: "addition", layer: 3 },
    { concept: "equation/variable literacy", layer: 4, is_floor: true },
  ],
  edges: [
    { concept: "Kepler's third law", requires: "proportionality", why: "T² ∝ r³ is a proportionality statement" },
    { concept: "Kepler's third law", requires: "powers/exponents", why: "squared and cubed are powers" },
    { concept: "Kepler's third law", requires: "ratio", why: "T²/r³ = constant is a ratio" },
    { concept: "proportionality", requires: "division", why: "scaling one quantity with another is a division" },
    { concept: "proportionality", requires: "constant", why: "'is proportional to' means the ratio is a fixed constant" },
    { concept: "powers/exponents", requires: "multiplication", why: "a power is repeated multiplication" },
    { concept: "ratio", requires: "division", why: "a ratio is the division of two quantities" },
    { concept: "division", requires: "multiplication", why: "division is the inverse of multiplication" },
    { concept: "division", requires: "equals sign as balance", why: "dividing both sides keeps the equation balanced" },
    { concept: "multiplication", requires: "addition", why: "multiplication is repeated addition" },
    { concept: "addition", requires: "equation/variable literacy", why: "addition combines values denoted by symbols" },
    { concept: "equals sign as balance", requires: "equation/variable literacy", why: "= means both sides are equal" },
  ],
};

const BAKED = { "kepler's third law": KEPLER };

// Decompose a topic. If `llm` (async (prompt, topic) => jsonString) is given, the
// LLM does the work (production path). Offline, fall back to a baked example.
export async function decompose(topic, { llm } = {}) {
  if (llm) {
    const raw = await llm(DECOMPOSITION_PROMPT, topic);
    const parsed = typeof raw === "string" ? JSON.parse(raw) : raw;
    return normalize(parsed);
  }
  const baked = BAKED[topic.toLowerCase().trim()];
  if (baked) return normalize(baked);
  throw new Error(`No LLM supplied and no baked example for "${topic}". In production the LLM decomposes via DECOMPOSITION_PROMPT.`);
}

// Validate/normalize the decomposition (whoever produced it).
export function normalize(d) {
  if (!d || !Array.isArray(d.nodes) || !Array.isArray(d.edges)) throw new Error("decomposition must have nodes[] and edges[]");
  return {
    topic: d.topic,
    nodes: d.nodes.map((n) => ({ concept: String(n.concept), layer: Number(n.layer ?? 0), is_floor: !!n.is_floor })),
    edges: d.edges.map((e) => ({ concept: String(e.concept), requires: String(e.requires), why: e.why ? String(e.why) : null })),
  };
}
