import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express, { type Request, type Response } from "express";
import cors from "cors";
import { z } from "zod";

import { AIAS_PROMPT } from "./content/aias.js";
import { getEMLArchitectPrompt } from "./content/eml.js";
import {
  INTERACTIVE_BUILDER_PHASE1_PROMPT,
  INTERACTIVE_BUILDER_PHASE2_PROMPT,
} from "./content/interactive-builder.js";
import { AUTONOMY_COACH_PROMPT } from "./content/autonomy.js";
import { ENGAGEMENT_OPENER_PROMPT } from "./content/engagement.js";
import { PASSION_CONNECTOR_PROMPT } from "./content/passion.js";
import { getOptimizerPrompt } from "./content/optimizer.js";
import {
  HABITS,
  WORKFLOWS,
  getHabit,
  getWorkflow,
  formatHabit,
  formatWorkflow,
  formatList,
} from "./content/em-field-guide.js";

// ─── Server factory ───────────────────────────────────────────────────────────
// Stateless mode: each MCP request gets a fresh server + transport. This
// matches OpenAI's recommended pattern for ChatGPT MCP connectors and avoids
// session-state issues during validator probes.

function createMcpServer(): McpServer {
  const server = new McpServer({
    name: "sids-eml-studio-mcp",
    version: "1.0.0",
  });

  registerPromptsAndTools(server);
  return server;
}

function registerPromptsAndTools(server: McpServer): void {

// ─── Prompt: AIAS Advisor ─────────────────────────────────────────────────────

server.prompt(
  "aias-advisor",
  "AI Assessment Scale Advisor — helps educators redesign homework and assessments using the 5-level AI Assessment Scale (AIAS). Produces full redesigns with student-facing instructions, rubrics, and safeguards.",
  {
    subject: z
      .string()
      .optional()
      .describe('Subject area (e.g., "Engineering", "Biology", "Writing")'),
    level: z
      .string()
      .optional()
      .describe('Student level (e.g., "undergraduate", "graduate", "high school")'),
  },
  async ({ subject, level }) => {
    let prompt = AIAS_PROMPT;

    if (subject || level) {
      const ctx = [level, subject].filter(Boolean).join(" ");
      prompt +=
        `\n\nContext note: The educator is working with a ${ctx} course. ` +
        `Tailor your recommendations accordingly.`;
    }

    return {
      messages: [{ role: "user" as const, content: { type: "text" as const, text: prompt } }],
    };
  }
);

// ─── Prompt: EML Architect ────────────────────────────────────────────────────

server.prompt(
  "eml-architect",
  "EML Architect — converts traditional textbook problems into Entrepreneurial Mindset Learning (EML) tasks. Preserves full technical rigor while cultivating habits of curiosity, connections, creating value, and action orientation. Includes all reference materials: Habits of EM, Curiosity Methods, Mindset Methods, EM Openers, and Adaptable EML Ideas.",
  {
    em_habits: z
      .string()
      .optional()
      .describe(
        'Comma-separated EM habits to focus on, e.g. "Curiosity, Creating Value". If omitted, the AI selects appropriate habits.'
      ),
    problems: z
      .string()
      .optional()
      .describe(
        "Paste the textbook problem(s) to reframe here. Alternatively, paste them in your message after activating this prompt."
      ),
  },
  async ({ em_habits, problems }) => {
    let prompt = getEMLArchitectPrompt(em_habits);

    if (problems) {
      prompt += `\n\n<PROBLEMS>\n${problems}\n</PROBLEMS>`;
    }

    return {
      messages: [{ role: "user" as const, content: { type: "text" as const, text: prompt } }],
    };
  }
);

// ─── Prompt: Interactive Builder — Phase 1 (Planning) ────────────────────────

server.prompt(
  "interactive-builder-planning",
  "Interactive Builder Phase 1 — guides faculty through designing a stateless, privacy-safe educational web-app. No code yet; produces a Final Blueprint Summary ready for Phase 2.",
  async () => ({
    messages: [
      {
        role: "user" as const,
        content: { type: "text" as const, text: INTERACTIVE_BUILDER_PHASE1_PROMPT },
      },
    ],
  })
);

// ─── Prompt: Interactive Builder — Phase 2 (Coding) ──────────────────────────

server.prompt(
  "interactive-builder-coding",
  "Interactive Builder Phase 2 — takes the blueprint from Phase 1 and builds a working single-file HTML prototype. Responsive, no backend, no data collection, openable by double-clicking index.html.",
  async () => ({
    messages: [
      {
        role: "user" as const,
        content: { type: "text" as const, text: INTERACTIVE_BUILDER_PHASE2_PROMPT },
      },
    ],
  })
);

// ─── Prompt: Autonomy Coach ───────────────────────────────────────────────────

server.prompt(
  "autonomy-coach",
  "Course Autonomy Coach — helps university instructors embed student autonomy into courses using 20 proven strategies (menu assignments, specs grading, branching labs, etc.) while maintaining academic standards.",
  {
    course_subject: z
      .string()
      .optional()
      .describe('Subject area (e.g., "Fluid Mechanics", "Technical Writing")'),
    course_level: z
      .string()
      .optional()
      .describe('Level (e.g., "introductory undergraduate", "senior capstone")'),
  },
  async ({ course_subject, course_level }) => {
    let prompt = AUTONOMY_COACH_PROMPT;

    if (course_subject || course_level) {
      const ctx = [course_level, course_subject].filter(Boolean).join(" ");
      prompt +=
        `\n\nContext note: The instructor is teaching a ${ctx} course. ` +
        `Adapt all recommendations to this discipline and level.`;
    }

    return {
      messages: [{ role: "user" as const, content: { type: "text" as const, text: prompt } }],
    };
  }
);

// ─── Prompt: Engagement Opener ────────────────────────────────────────────────

server.prompt(
  "engagement-opener",
  "Joyful Opener Designer — creates a 3-minute classroom micro-experiment that sparks curiosity through cognitive dissonance, sensory surprise, or collaborative discovery. Produces a copy-ready worksheet section.",
  {
    course_title: z
      .string()
      .optional()
      .describe('Course name and level (e.g., "Statics, sophomore engineering")'),
    concept: z
      .string()
      .optional()
      .describe('Specific concept being introduced (e.g., "free body diagrams", "osmosis")'),
  },
  async ({ course_title, concept }) => {
    let prompt = ENGAGEMENT_OPENER_PROMPT;

    if (course_title || concept) {
      const parts: string[] = [];
      if (course_title) parts.push(`Course: ${course_title}`);
      if (concept) parts.push(`Concept: ${concept}`);
      prompt += `\n\nContext note: Skip the intake question for the following — ${parts.join("; ")}. Proceed directly to generating three options.`;
    }

    return {
      messages: [{ role: "user" as const, content: { type: "text" as const, text: prompt } }],
    };
  }
);

// ─── Prompt: Passion Connector ────────────────────────────────────────────────

server.prompt(
  "passion-connector",
  "Passion Connector — helps educators design a 5-minute classroom segment that authentically connects their personal passion to course content. Produces two low-prep, ready-to-use ideas with sentence starters.",
  {
    passion: z
      .string()
      .optional()
      .describe(
        'The educator\'s passion, interest, or hobby (e.g., "rock climbing", "jazz music", "cooking")'
      ),
    course: z
      .string()
      .optional()
      .describe('The course or lesson focus (e.g., "Thermodynamics", "Technical Writing 101")'),
  },
  async ({ passion, course }) => {
    let prompt = PASSION_CONNECTOR_PROMPT;

    if (passion || course) {
      const parts: string[] = [];
      if (passion) parts.push(`[X] = ${passion}`);
      if (course) parts.push(`[Y] = ${course}`);
      prompt += `\n\nContext note: Skip the intake questions. The user has provided: ${parts.join("; ")}. Proceed directly to generating two classroom segment ideas.`;
    }

    return {
      messages: [{ role: "user" as const, content: { type: "text" as const, text: prompt } }],
    };
  }
);

// ─── Prompt: Prompt Optimizer ─────────────────────────────────────────────────

server.prompt(
  "prompt-optimizer",
  "Prompt Optimizer — rewrites rough prompts into precise, production-ready system prompts for Claude, Gemini, or GPT. Includes model-specific best practices. Returns only the upgraded prompt in a code block.",
  {
    target_model: z
      .enum(["Claude", "Gemini", "GPT", "model-agnostic"])
      .optional()
      .describe('Target AI model. Defaults to "model-agnostic" if not specified.'),
    raw_prompt: z
      .string()
      .optional()
      .describe(
        "The rough prompt to optimize. Alternatively, paste it in your message after activating this prompt."
      ),
    optional_context: z
      .string()
      .optional()
      .describe("Additional context about the use case or audience."),
  },
  async ({ target_model, raw_prompt, optional_context }) => {
    const prompt = getOptimizerPrompt(target_model, raw_prompt, optional_context);

    return {
      messages: [{ role: "user" as const, content: { type: "text" as const, text: prompt } }],
    };
  }
);

// ─── Tools (mirror of prompts, for clients like ChatGPT) ──────────────────────
// Each tool uses registerTool with explicit annotations
// (readOnlyHint, openWorldHint, destructiveHint) which ChatGPT requires.

const textResult = (text: string) => ({
  content: [{ type: "text" as const, text }],
});

const READ_ONLY_ANNOTATIONS = {
  readOnlyHint: true,
  openWorldHint: false,
  destructiveHint: false,
  idempotentHint: true,
};

server.registerTool(
  "aias_advisor",
  {
    title: "AIAS Advisor",
    description:
      "Returns a system prompt that turns the assistant into an AI Assessment Scale Advisor, helping educators redesign homework using the 5-level AIAS framework. Use the returned text as operating instructions for the rest of the conversation.",
    inputSchema: {
      subject: z.string().optional().describe('Subject area (e.g., "Engineering", "Biology")'),
      level: z.string().optional().describe('Student level (e.g., "undergraduate")'),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ subject, level }) => {
    let prompt = AIAS_PROMPT;
    if (subject || level) {
      const ctx = [level, subject].filter(Boolean).join(" ");
      prompt += `\n\nContext note: The educator is working with a ${ctx} course. Tailor your recommendations accordingly.`;
    }
    return textResult(prompt);
  }
);

server.registerTool(
  "eml_architect",
  {
    title: "EML Architect",
    description:
      "Returns a system prompt that turns the assistant into an Entrepreneurial Mindset Learning Architect, converting textbook problems into EM learning tasks. Includes full reference materials (Habits of EM, Curiosity Methods, Mindset Methods, EM Openers, Adaptable EML Ideas).",
    inputSchema: {
      em_habits: z.string().optional().describe('EM habits to focus on, e.g. "Curiosity, Creating Value"'),
      problems: z.string().optional().describe("Textbook problem(s) to reframe"),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ em_habits, problems }) => {
    let prompt = getEMLArchitectPrompt(em_habits);
    if (problems) prompt += `\n\n<PROBLEMS>\n${problems}\n</PROBLEMS>`;
    return textResult(prompt);
  }
);

server.registerTool(
  "interactive_builder_planning",
  {
    title: "Interactive Builder — Planning",
    description:
      "Returns a system prompt that guides faculty through designing a stateless, privacy-safe educational web-app. Produces a Final Blueprint Summary ready for the coding phase.",
    inputSchema: {},
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async () => textResult(INTERACTIVE_BUILDER_PHASE1_PROMPT)
);

server.registerTool(
  "interactive_builder_coding",
  {
    title: "Interactive Builder — Coding",
    description:
      "Returns a system prompt that takes a blueprint from the planning phase and builds a working single-file HTML prototype.",
    inputSchema: {},
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async () => textResult(INTERACTIVE_BUILDER_PHASE2_PROMPT)
);

server.registerTool(
  "autonomy_coach",
  {
    title: "Course Autonomy Coach",
    description:
      "Returns a system prompt that helps university instructors embed student autonomy into courses using 20 proven strategies.",
    inputSchema: {
      course_subject: z.string().optional().describe('Subject area (e.g., "Fluid Mechanics")'),
      course_level: z.string().optional().describe('Level (e.g., "introductory undergraduate")'),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ course_subject, course_level }) => {
    let prompt = AUTONOMY_COACH_PROMPT;
    if (course_subject || course_level) {
      const ctx = [course_level, course_subject].filter(Boolean).join(" ");
      prompt += `\n\nContext note: The instructor is teaching a ${ctx} course. Adapt all recommendations to this discipline and level.`;
    }
    return textResult(prompt);
  }
);

server.registerTool(
  "engagement_opener",
  {
    title: "Joyful Opener Designer",
    description:
      "Returns a system prompt that creates a 3-minute classroom micro-experiment sparking curiosity through cognitive dissonance, sensory surprise, or collaborative discovery.",
    inputSchema: {
      course_title: z.string().optional().describe("Course name and level"),
      concept: z.string().optional().describe("Specific concept being introduced"),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ course_title, concept }) => {
    let prompt = ENGAGEMENT_OPENER_PROMPT;
    if (course_title || concept) {
      const parts: string[] = [];
      if (course_title) parts.push(`Course: ${course_title}`);
      if (concept) parts.push(`Concept: ${concept}`);
      prompt += `\n\nContext note: Skip the intake question. ${parts.join("; ")}. Proceed directly to generating three options.`;
    }
    return textResult(prompt);
  }
);

server.registerTool(
  "passion_connector",
  {
    title: "Passion Connector",
    description:
      "Returns a system prompt that helps educators design a 5-minute classroom segment linking their personal passion to course content.",
    inputSchema: {
      passion: z.string().optional().describe("The educator's passion or hobby"),
      course: z.string().optional().describe("The course or lesson focus"),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ passion, course }) => {
    let prompt = PASSION_CONNECTOR_PROMPT;
    if (passion || course) {
      const parts: string[] = [];
      if (passion) parts.push(`[X] = ${passion}`);
      if (course) parts.push(`[Y] = ${course}`);
      prompt += `\n\nContext note: Skip the intake questions. ${parts.join("; ")}. Proceed directly to generating two classroom segment ideas.`;
    }
    return textResult(prompt);
  }
);

server.registerTool(
  "prompt_optimizer",
  {
    title: "Prompt Optimizer",
    description:
      "Returns a system prompt that rewrites rough prompts into precise, production-ready prompts for Claude, Gemini, or GPT.",
    inputSchema: {
      target_model: z
        .enum(["Claude", "Gemini", "GPT", "model-agnostic"])
        .optional()
        .describe("Target AI model"),
      raw_prompt: z.string().optional().describe("The rough prompt to optimize"),
      optional_context: z.string().optional().describe("Additional context"),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ target_model, raw_prompt, optional_context }) => {
    return textResult(getOptimizerPrompt(target_model, raw_prompt, optional_context));
  }
);

  // ─── EM × AI Field Guide ────────────────────────────────────────────────────
  // The 18 KEEN Habits of Entrepreneurial Mindset for an age of AI, plus 7
  // workflows. Content lives in ./content/em-field-guide.ts (canonical, from
  // context.md). Names accepted case- and punctuation-insensitively.

  const HABIT_NAMES = Object.keys(HABITS);
  const WORKFLOW_NAMES = Object.keys(WORKFLOWS);

  server.registerTool(
    "em_list",
    {
      title: "EM Field Guide — Map",
      description:
        "Returns the full map of the EM × AI Field Guide: the 3 families (Curiosity, Connections, Creating Value), all 18 KEEN habits with their one-line tensions, and the 7 workflows. Start here to see what's available, then call em_habit or em_workflow for full content.",
      inputSchema: {},
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async () => textResult(formatList())
  );

  server.registerTool(
    "em_habit",
    {
      title: "EM Habit",
      description:
        `Returns the full content for one of the 18 KEEN entrepreneurial-mindset habits: its family, definition, named frameworks, the AI-era move, how AI helps build it, the anti-pattern, the one-line tension, the Run-it-yourself paste-ready prompt, and the Run-it-with-students blueprint. Valid habits: ${HABIT_NAMES.join(", ")}.`,
      inputSchema: {
        name: z.string().describe(`The habit name, e.g. "Systems Thinking" or "Contrarian Thinking". One of: ${HABIT_NAMES.join(", ")}`),
      },
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async ({ name }) => {
      const habit = getHabit(name);
      if (!habit) {
        return textResult(
          `No habit named "${name}". Valid habits are: ${HABIT_NAMES.join(", ")}. Call em_list to see the full map.`
        );
      }
      return textResult(formatHabit(habit));
    }
  );

  server.registerTool(
    "em_coach",
    {
      title: "EM Habit Coach",
      description:
        `Returns just the Run-it-yourself paste-ready prompt for a habit (plus its framing: what it does, when to use it, what good output looks like). Use this when you want to run a habit on your own task right now. Valid habits: ${HABIT_NAMES.join(", ")}.`,
      inputSchema: {
        habit: z.string().describe(`The habit name to coach, e.g. "Risk Awareness". One of: ${HABIT_NAMES.join(", ")}`),
      },
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async ({ habit }) => {
      const h = getHabit(habit);
      if (!h) {
        return textResult(
          `No habit named "${habit}". Valid habits are: ${HABIT_NAMES.join(", ")}. Call em_list to see the full map.`
        );
      }
      const r = h.runItYourself;
      return textResult(
        `# ${h.name} — Run it yourself\n\n**What it does:** ${r.whatItDoes}\n**When to use it:** ${r.whenToUse}\n**What good output looks like:** ${r.whatGoodOutputLooksLike}\n\n**Prompt (paste-ready):**\n\`\`\`\n${r.prompt}\n\`\`\``
      );
    }
  );

  server.registerTool(
    "em_workflow",
    {
      title: "EM Workflow",
      description:
        `Returns a full multi-habit workflow: the habits it composes, when to reach for it, the Run-it-yourself orchestration prompt (a system prompt with a pause-after-each-step contract), the Run-it-with-students blueprint, and the meta-prompt to build a class activity. Valid workflows: ${WORKFLOW_NAMES.join(", ")}.`,
      inputSchema: {
        name: z.string().describe(`The workflow name, e.g. "Assumption Buster" or "Reality Check". One of: ${WORKFLOW_NAMES.join(", ")}`),
      },
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async ({ name }) => {
      const workflow = getWorkflow(name);
      if (!workflow) {
        return textResult(
          `No workflow named "${name}". Valid workflows are: ${WORKFLOW_NAMES.join(", ")}. Call em_list to see the full map.`
        );
      }
      return textResult(formatWorkflow(workflow));
    }
  );

  server.registerTool(
    "em_diagnostic",
    {
      title: "EM × AI Diagnostic",
      description:
        "Returns the EM × AI Diagnostic orchestration prompt. Start here when you don't yet know which habit or workflow you need — it assesses your AI practice across all three Cs and routes you to the right tool. Use the returned text as your operating instructions.",
      inputSchema: {},
      annotations: READ_ONLY_ANNOTATIONS,
    },
    async () => {
      const diagnostic = getWorkflow("EM × AI Diagnostic");
      if (!diagnostic) return textResult("Diagnostic content unavailable.");
      return textResult(diagnostic.pm);
    }
  );

  // ─── EM × AI Field Guide prompts (Claude slash-menu parity) ──────────────────

  const promptMessage = (text: string) => ({
    messages: [{ role: "user" as const, content: { type: "text" as const, text } }],
  });

  server.prompt(
    "em-list",
    "EM Field Guide map — the 3 families, 18 KEEN habits with their tensions, and 7 workflows. Start here to browse what's available.",
    async () => promptMessage(formatList())
  );

  server.prompt(
    "em-habit",
    "Full content for one of the 18 KEEN entrepreneurial-mindset habits (frameworks, AI-era move, anti-pattern, Run-it-yourself prompt, Run-it-with-students blueprint).",
    { name: z.string().describe(`Habit name, e.g. "Systems Thinking". One of: ${Object.keys(HABITS).join(", ")}`) },
    async ({ name }) => {
      const habit = getHabit(name);
      return promptMessage(
        habit
          ? formatHabit(habit)
          : `No habit named "${name}". Valid habits: ${Object.keys(HABITS).join(", ")}.`
      );
    }
  );

  server.prompt(
    "em-coach",
    "Just the Run-it-yourself paste-ready prompt for a habit, ready to run on your own task.",
    { habit: z.string().describe(`Habit name, e.g. "Risk Awareness". One of: ${Object.keys(HABITS).join(", ")}`) },
    async ({ habit }) => {
      const h = getHabit(habit);
      if (!h) return promptMessage(`No habit named "${habit}". Valid habits: ${Object.keys(HABITS).join(", ")}.`);
      const r = h.runItYourself;
      return promptMessage(
        `# ${h.name} — Run it yourself\n\n**What it does:** ${r.whatItDoes}\n**When to use it:** ${r.whenToUse}\n**What good output looks like:** ${r.whatGoodOutputLooksLike}\n\n**Prompt:**\n${r.prompt}`
      );
    }
  );

  server.prompt(
    "em-workflow",
    "Full multi-habit workflow: orchestration prompt with pause-after-each-step contract, plus the Run-it-with-students blueprint and build-an-activity meta-prompt.",
    { name: z.string().describe(`Workflow name, e.g. "Assumption Buster". One of: ${Object.keys(WORKFLOWS).join(", ")}`) },
    async ({ name }) => {
      const workflow = getWorkflow(name);
      return promptMessage(
        workflow
          ? formatWorkflow(workflow)
          : `No workflow named "${name}". Valid workflows: ${Object.keys(WORKFLOWS).join(", ")}.`
      );
    }
  );

  server.prompt(
    "em-diagnostic",
    "EM × AI Diagnostic — assesses your AI practice across all three Cs and routes you to the right habit or workflow. Start here if unsure where to begin.",
    async () => {
      const diagnostic = getWorkflow("EM × AI Diagnostic");
      return promptMessage(diagnostic ? diagnostic.pm : "Diagnostic content unavailable.");
    }
  );

} // ─── end registerPromptsAndTools ─────────────────────────────────────────────

// ─── HTTP Server ──────────────────────────────────────────────────────────────

const app = express();

// CORS — allow any origin (this is a public, unauthenticated service)
app.use(
  cors({
    origin: "*",
    exposedHeaders: ["mcp-session-id"],
    allowedHeaders: ["Content-Type", "Accept", "mcp-session-id", "mcp-protocol-version", "Authorization"],
    methods: ["GET", "POST", "DELETE", "OPTIONS"],
  })
);
app.options("*", cors());

app.use(express.json({ limit: "4mb" }));

// Health check (browser-friendly)
app.get("/", (_req: Request, res: Response) => {
  res.json({
    name: "Sid's EML Studio MCP Server",
    version: "1.0.0",
    mcp_endpoint: "/mcp",
    tools: [
      "aias_advisor",
      "eml_architect",
      "interactive_builder_planning",
      "interactive_builder_coding",
      "autonomy_coach",
      "engagement_opener",
      "passion_connector",
      "prompt_optimizer",
      "em_list",
      "em_habit",
      "em_coach",
      "em_workflow",
      "em_diagnostic",
    ],
    status: "ok",
  });
});

// OAuth discovery probes — return clean 404 JSON so ChatGPT knows there's no
// OAuth/DCR rather than getting Express's HTML 404 page (which can confuse
// the validator).
const oauthProbe = (_req: Request, res: Response) => {
  res.status(404).json({ error: "not_found", error_description: "this server uses no authentication" });
};
app.get("/.well-known/oauth-authorization-server", oauthProbe);
app.get("/.well-known/oauth-protected-resource", oauthProbe);
app.get("/.well-known/openid-configuration", oauthProbe);

// Main MCP endpoint — stateless POST handling.
// Each request gets its own server + transport, then both close.
app.post("/mcp", async (req: Request, res: Response) => {
  try {
    const server = createMcpServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined, // stateless: no session ID required
      enableJsonResponse: true,
    });

    res.on("close", () => {
      transport.close();
      server.close();
    });

    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (err) {
    console.error("MCP POST error:", err);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: "2.0",
        error: { code: -32603, message: "Internal server error" },
        id: null,
      });
    }
  }
});

// In stateless mode, GET and DELETE are not used. Respond 405.
app.get("/mcp", (_req: Request, res: Response) => {
  res.status(405).json({
    jsonrpc: "2.0",
    error: { code: -32000, message: "Method not allowed in stateless mode. Use POST." },
    id: null,
  });
});

app.delete("/mcp", (_req: Request, res: Response) => {
  res.status(405).json({
    jsonrpc: "2.0",
    error: { code: -32000, message: "Method not allowed in stateless mode." },
    id: null,
  });
});

const PORT = parseInt(process.env.PORT ?? "3000", 10);
app.listen(PORT, () => {
  console.log(`Sid's EML Studio MCP Server running on port ${PORT}`);
  console.log(`MCP endpoint: http://localhost:${PORT}/mcp`);
});
