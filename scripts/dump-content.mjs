// Dumps all prompt content from the built TypeScript modules into content.json,
// which the Python FastMCP server (server.py) loads at startup. Run after any
// content change:  npm run build && node scripts/dump-content.mjs
import { writeFileSync } from "fs";

import { AIAS_PROMPT } from "../dist/content/aias.js";
import { getEMLArchitectPrompt } from "../dist/content/eml.js";
import {
  INTERACTIVE_BUILDER_PHASE1_PROMPT,
  INTERACTIVE_BUILDER_PHASE2_PROMPT,
} from "../dist/content/interactive-builder.js";
import { AUTONOMY_COACH_PROMPT } from "../dist/content/autonomy.js";
import { ENGAGEMENT_OPENER_PROMPT } from "../dist/content/engagement.js";
import { PASSION_CONNECTOR_PROMPT } from "../dist/content/passion.js";
import {
  OPTIMIZER_BASE_PROMPT,
  CLAUDE_BEST_PRACTICES,
  GPT_BEST_PRACTICES,
} from "../dist/content/optimizer.js";
import {
  HABITS,
  WORKFLOWS,
  formatHabit,
  formatWorkflow,
  formatList,
} from "../dist/content/em-field-guide.js";

const coachText = (h) => {
  const r = h.runItYourself;
  return `# ${h.name} — Run it yourself\n\n**What it does:** ${r.whatItDoes}\n**When to use it:** ${r.whenToUse}\n**What good output looks like:** ${r.whatGoodOutputLooksLike}\n\n**Prompt (paste-ready):**\n\`\`\`\n${r.prompt}\n\`\`\``;
};

const content = {
  aias: AIAS_PROMPT,
  eml_full: getEMLArchitectPrompt(), // habit-focus injection is re-done in Python via string replace
  interactive_builder_planning: INTERACTIVE_BUILDER_PHASE1_PROMPT,
  interactive_builder_coding: INTERACTIVE_BUILDER_PHASE2_PROMPT,
  autonomy: AUTONOMY_COACH_PROMPT,
  engagement: ENGAGEMENT_OPENER_PROMPT,
  passion: PASSION_CONNECTOR_PROMPT,
  optimizer: {
    base: OPTIMIZER_BASE_PROMPT,
    claude_bp: CLAUDE_BEST_PRACTICES,
    gpt_bp: GPT_BEST_PRACTICES,
  },
  em: {
    list: formatList(),
    habits: Object.fromEntries(
      Object.values(HABITS).map((h) => [h.name, { full: formatHabit(h), coach: coachText(h) }])
    ),
    workflows: Object.fromEntries(
      Object.values(WORKFLOWS).map((w) => [w.name, { full: formatWorkflow(w), pm: w.pm }])
    ),
  },
};

writeFileSync(new URL("../content.json", import.meta.url), JSON.stringify(content, null, 1));
console.log(
  `content.json written: ${Object.keys(content.em.habits).length} habits, ${Object.keys(content.em.workflows).length} workflows`
);
