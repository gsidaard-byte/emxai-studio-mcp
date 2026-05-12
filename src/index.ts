import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express, { type Request, type Response } from "express";
import { randomUUID } from "crypto";
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

// ─── Server setup ─────────────────────────────────────────────────────────────

const server = new McpServer({
  name: "sids-eml-studio-mcp",
  version: "1.0.0",
});

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

// ─── Tools (mirror of prompts, for clients that don't support MCP prompts) ───
// ChatGPT's MCP connector currently requires tools rather than prompts.
// Each tool returns the same content as its corresponding prompt.

const textResult = (text: string) => ({
  content: [{ type: "text" as const, text }],
});

server.tool(
  "aias_advisor",
  "AI Assessment Scale Advisor — returns a system prompt that helps educators redesign homework using the 5-level AI Assessment Scale (AIAS). Use the returned text as your operating instructions for the rest of the conversation.",
  {
    subject: z.string().optional().describe('Subject area (e.g., "Engineering", "Biology")'),
    level: z.string().optional().describe('Student level (e.g., "undergraduate")'),
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

server.tool(
  "eml_architect",
  "EML Architect — returns a system prompt that converts traditional textbook problems into Entrepreneurial Mindset Learning (EML) tasks. Includes all reference materials (Habits of EM, Curiosity Methods, Mindset Methods, EM Openers, Adaptable EML Ideas). Use the returned text as your operating instructions.",
  {
    em_habits: z.string().optional().describe('EM habits to focus on, e.g. "Curiosity, Creating Value"'),
    problems: z.string().optional().describe("Textbook problem(s) to reframe"),
  },
  async ({ em_habits, problems }) => {
    let prompt = getEMLArchitectPrompt(em_habits);
    if (problems) prompt += `\n\n<PROBLEMS>\n${problems}\n</PROBLEMS>`;
    return textResult(prompt);
  }
);

server.tool(
  "interactive_builder_planning",
  "Interactive Builder Phase 1 — returns a system prompt that guides faculty through designing a stateless, privacy-safe educational web-app. Produces a Final Blueprint Summary. Use the returned text as your operating instructions.",
  {},
  async () => textResult(INTERACTIVE_BUILDER_PHASE1_PROMPT)
);

server.tool(
  "interactive_builder_coding",
  "Interactive Builder Phase 2 — returns a system prompt that takes a blueprint from Phase 1 and builds a working single-file HTML prototype. Use the returned text as your operating instructions.",
  {},
  async () => textResult(INTERACTIVE_BUILDER_PHASE2_PROMPT)
);

server.tool(
  "autonomy_coach",
  "Course Autonomy Coach — returns a system prompt that helps university instructors embed student autonomy into courses using 20 proven strategies. Use the returned text as your operating instructions.",
  {
    course_subject: z.string().optional().describe('Subject area (e.g., "Fluid Mechanics")'),
    course_level: z.string().optional().describe('Level (e.g., "introductory undergraduate")'),
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

server.tool(
  "engagement_opener",
  "Joyful Opener Designer — returns a system prompt that creates a 3-minute classroom micro-experiment sparking curiosity through cognitive dissonance, sensory surprise, or collaborative discovery. Use the returned text as your operating instructions.",
  {
    course_title: z.string().optional().describe('Course name and level'),
    concept: z.string().optional().describe('Specific concept being introduced'),
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

server.tool(
  "passion_connector",
  "Passion Connector — returns a system prompt that helps educators design a 5-minute classroom segment linking their personal passion to course content. Use the returned text as your operating instructions.",
  {
    passion: z.string().optional().describe("The educator's passion or hobby"),
    course: z.string().optional().describe("The course or lesson focus"),
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

server.tool(
  "prompt_optimizer",
  "Prompt Optimizer — returns a system prompt that rewrites rough prompts into precise, production-ready prompts for Claude, Gemini, or GPT. Use the returned text as your operating instructions.",
  {
    target_model: z.enum(["Claude", "Gemini", "GPT", "model-agnostic"]).optional().describe('Target AI model'),
    raw_prompt: z.string().optional().describe("The rough prompt to optimize"),
    optional_context: z.string().optional().describe("Additional context"),
  },
  async ({ target_model, raw_prompt, optional_context }) => {
    return textResult(getOptimizerPrompt(target_model, raw_prompt, optional_context));
  }
);

// ─── HTTP Server ──────────────────────────────────────────────────────────────

const app = express();
app.use(express.json());

// Store active transports by session ID
const transports = new Map<string, StreamableHTTPServerTransport>();

// Health check
app.get("/", (_req: Request, res: Response) => {
  res.json({
    name: "Sid's EML Studio MCP Server",
    version: "1.0.0",
    prompts: [
      "aias-advisor",
      "eml-architect",
      "interactive-builder-planning",
      "interactive-builder-coding",
      "autonomy-coach",
      "engagement-opener",
      "passion-connector",
      "prompt-optimizer",
    ],
    status: "ok",
  });
});

// Main MCP endpoint — POST (new requests and messages)
app.post("/mcp", async (req: Request, res: Response) => {
  const sessionId = (req.headers["mcp-session-id"] as string) || randomUUID();

  let transport = transports.get(sessionId);

  if (!transport) {
    transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: () => sessionId,
      onsessioninitialized: (id) => {
        transports.set(id, transport!);
      },
    });

    transport.onclose = () => {
      transports.delete(sessionId);
    };

    await server.connect(transport);
  }

  await transport.handleRequest(req, res, req.body);
});

// SSE stream for server-sent events (GET)
app.get("/mcp", async (req: Request, res: Response) => {
  const sessionId = req.headers["mcp-session-id"] as string;

  if (!sessionId || !transports.has(sessionId)) {
    res.status(400).json({ error: "No active session. Send a POST to /mcp first." });
    return;
  }

  const transport = transports.get(sessionId)!;
  await transport.handleRequest(req, res);
});

// Session termination (DELETE)
app.delete("/mcp", async (req: Request, res: Response) => {
  const sessionId = req.headers["mcp-session-id"] as string;

  if (sessionId && transports.has(sessionId)) {
    const transport = transports.get(sessionId)!;
    await transport.handleRequest(req, res);
    transports.delete(sessionId);
  } else {
    res.status(200).json({ success: true });
  }
});

const PORT = parseInt(process.env.PORT ?? "3000", 10);
app.listen(PORT, () => {
  console.log(`Sid's EML Studio MCP Server running on port ${PORT}`);
  console.log(`MCP endpoint: http://localhost:${PORT}/mcp`);
});
