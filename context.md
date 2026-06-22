# EM × AI Field Guide — Context for Updating the SidsEMLStudio MCP Server

> Handoff document for Claude Code / Claude Cowork. It carries the canonical, current content from the EM × AI Field Guide so the MCP server can be brought in sync. Everything below is the source of truth as of this handoff. Where the server and this document disagree, this document wins.

## 1. What this is and why you're reading it

Dr. Sid Gunasekaran maintains an interactive HTML artifact called **The EM × AI Field Guide**. It teaches the 18 KEEN Habits of Entrepreneurial Mindset for an age of AI, written for engineering faculty who both practice these habits themselves and teach them. The guide was iteratively deepened over a long working session. The content has moved well beyond what the existing MCP server (`SidsEMLStudio`, a FastMCP server, also referenced as `em_ai_server.py` / `em_ai_data.py`) currently holds.

Your job is to update that MCP server so its tools return the **current** content captured here. This document gives you the canonical text for all 18 habits and all 7 workflows, plus the structural changes that happened, so you can reconcile the server's data module against it.

## 2. The vocabulary and structure you must preserve

The guide is organized as **3 families (the 3Cs) → 18 habits → 7 workflows**.

- **Curiosity**: Inquisitiveness, Contrarian Thinking, Opportunity Seeking, Experimentation, Confronting Ambiguity, Future-Minded
- **Connections**: Creativity, Systems Thinking, Knowledge Synthesis, Implications Thinking, Strategic Thinking, Risk Awareness
- **Creating Value**: Value Awareness, Customer-Centric Thinking, Impact Thinking, Socially Minded, Persistence, Resourcefulness

Each **habit** now carries two delivery modes, renamed from the old labels:
- **Run it yourself** (was *Model it*) — a paste-ready prompt the faculty member runs on their own task. Framed by three lines: *What it does*, *When to use it*, *What good output looks like*.
- **Run it with students** (was *Teach it*) — a strategy the faculty member designs and leads, expressed as a three-part blueprint: *Setup*, *AI's role*, *Assessed on*. It is **not** a prompt to paste.

Each **workflow** carries the same two modes:
- **Run it yourself** — a full orchestration system-prompt (the `pm` value) with a pause-after-each-step contract.
- **Run it with students** — a *Setup / AI's role / Assessed on* blueprint, plus a collapsible **Prompt to build this activity** (a faculty meta-prompt that has AI generate the brief, student instructions, and rubric).

## 3. The most important structural changes since the MCP was last built

1. **Habits are now framework-grounded.** Every habit names the established engineering/design methods it teaches (e.g. Systems Thinking → Iceberg Model, causal loop diagrams, stock-and-flow; Contrarian Thinking → Duncker diagram, Six Thinking Hats, Janusian thinking). The `frameworks` field is new and the `fosters` text now references those named methods. This was the single biggest content change. If the MCP returns generic habit descriptions, they need replacing with the framework-grounded versions below.
2. **The master principle was professionalized.** Old: *"If you're bad at something, you can't judge it, so you'll approve clean garbage... build taste first."* New: *"You can't evaluate work in a domain you haven't mastered, so polished output reads as competent when it isn't. AI amplifies the judgment you bring. It cannot supply the judgment you lack. Develop expertise first, then let AI scale it. Never the reverse."* Replace every occurrence in the server.
3. **Workflow orchestration prompts (`pm`) were fully reworked** for tighter instruction-following: task stated first, numbered steps with the anti-pattern attached to each, an explicit *pause and wait after each step* contract, and a compact *operating frame*. Removed jargon throughout: **no** "steelman", "build taste", "red-team", "weird", or "MODE: MODEL-IT". The canonical reworked `pm` prompts are in section 6.
4. **Labels renamed**: *Model it → Run it yourself*, *Teach it → Run it with students*.
5. **Writing style** (apply to any new text you generate): no em-dashes, no colons in prose, no semicolons. Punchy declarative sentences. Faculty/user as agent, AI as instrument. Avoid the words "genuinely", "steelman", and "weird".

## 4. Suggested MCP tool surface

The existing server reportedly exposes tools like `em_coach`, `em_diagnostic`, and per-workflow tools. Reconcile them to return the content below. A reasonable target surface:

- `em_habit(name)` → returns a habit's family, definition, frameworks, the AI-era move, how AI helps build it, the anti-pattern, the one-line tension, and both modes (Run-it-yourself prompt with its three framing lines; Run-it-with-students blueprint).
- `em_coach(habit)` → returns the Run-it-yourself prompt for a habit, ready to run.
- `em_diagnostic()` → returns the EM × AI Diagnostic orchestration prompt (section 6).
- `em_workflow(name)` → returns a workflow's habits, when-to-use line, the orchestration prompt (`pm`), the Run-it-with-students blueprint, and the build-this-activity meta-prompt.
- `em_list()` → returns the 3-family / 18-habit / 7-workflow map.

Keep whatever names already exist if they're load-bearing for Sid's other tools; the priority is the **content**, not the tool names.

## 5. Canonical habit content (all 18)

Each habit below gives every field the MCP should be able to return. Text is verbatim from the current guide.

### Inquisitiveness
- **Family**: Curiosity
- **Definition**: Applies curiosity about a continuously changing world.
- **Frameworks**: The Five Whys · Question Formulation Technique · First-principles decomposition
- **The AI-era move (Step 1)**: Stay close to reality. Inspect raw data, talk to people.
- **How AI helps build it (Step 2)**: AI can run the early stages of these methods at speed. Ask it for a first-principles decomposition of an unfamiliar system, a structured Five Whys chain to test, or the ten questions a skeptical expert would ask. Crucially, have it attach each question to the kind of primary source that would answer it, so the model becomes a map of what to verify rather than a substitute for verifying.
- **The anti-pattern to guard against (Step 3)**: Letting the AI summary stand in for the primary source. Your curiosity narrows to whatever the model surfaced, and you stop noticing the anomaly in the raw data.
- **One-line tension**: AI is a fast on-ramp to questions, but not a substitute for looking.

**Run it yourself (paste-ready prompt):**
- *What it does*: Turns AI into a fast on-ramp to a new field that points you back to primary sources instead of standing in for them.
- *When to use it*: You're entering an unfamiliar domain and need to get oriented without taking the AI's summary on faith.
- *What good output looks like*: Ten questions that expose what you don't know yet, each tied to a real source you can go verify. If it just hands you a tidy overview, it defeated the purpose.
- *Prompt*:
```text
I'm new to [domain]. Give me the 10 questions a skeptical expert would ask before trusting any claim in this area. For each question, tell me what kind of primary source would answer it - a paper, a dataset, a standard - so I can check it myself. Don't summarize the field for me, point me at what I should read.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Give students a topic outside their expertise and 20 minutes to map it with AI. Then they must verify three of the AI's claims against primary sources - the actual paper, dataset, or standard - and report one place where the AI was wrong, vague, or out of date. The verification is the assignment, not the map.
- *AI's role*: Maps unfamiliar territory fast, which is its real strength here. Students do the checking against real sources themselves, because the habit being built is the reflex to confirm before trusting, and that reflex dies if AI does the confirming too.
- *Assessed on*: The rigor of the three verifications and the specific error they caught, not how thorough the initial map looked.

### Contrarian Thinking
- **Family**: Curiosity
- **Definition**: Explores alternative or disruptive views of accepted solutions.
- **Frameworks**: The Duncker diagram · de Bono's Six Thinking Hats · Janusian thinking
- **The AI-era move (Step 1)**: Challenge assumptions.
- **How AI helps build it (Step 2)**: This is where AI becomes a real ideation partner. Have it build a Duncker diagram of your problem, mapping the functional alternatives that functional fixedness hid, then wear the Black Hat to critique each branch, or hold the Janusian opposite of your assumption. Its breadth across domains surfaces alternative means a single student would never list.
- **The anti-pattern to guard against (Step 3)**: AI is tuned to be agreeable. Used only as a helper, it reinforces the conventional view instead of disrupting it.
- **One-line tension**: AI defaults to agreeable, so make it argue against you.

**Run it yourself (paste-ready prompt):**
- *What it does*: Turns AI into a devil's advocate against your own decision so you find the weak point before someone else does.
- *When to use it*: You've made a design or strategic call and want it stress-tested before you commit.
- *What good output looks like*: A challenge sharp enough to make you pause, landing on one load-bearing assumption and a way to test it. If it flatters you, push it harder.
- *Prompt*:
```text
Make the strongest case you can that my approach to [X] is wrong. Argue the opposing view as hard as you can, don't hedge. Then name the single assumption I'm making that, if it turned out false, would break the whole thing. End by telling me what evidence would settle whether that assumption holds.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Students submit a design decision they've already made, then prompt AI to build the strongest possible case against it. They write a one-page memo that either defends the original decision or revises it, citing what the critique surfaced.
- *AI's role*: Generates the opposing case tirelessly and without ego, which a peer often won't. Students must judge whether the critique is sound and decide what to do, because the habit is weighing a challenge, not just receiving one.
- *Assessed on*: How well they evaluate the quality of the critique and justify their final call, not whether they changed their mind.

### Opportunity Seeking
- **Family**: Curiosity
- **Definition**: Identifies trends and unmet needs to uncover new opportunities.
- **Frameworks**: Jobs-to-be-Done · White-space gap analysis · The Kano model
- **The AI-era move (Step 1)**: Move up the value chain. Define the real problem.
- **How AI helps build it (Step 2)**: AI can build the white-space map at a speed no student can match, articulating the jobs current solutions are hired to do and which are well served. That clears the documented ground so your judgment can hunt the unserved job the map exposes.
- **The anti-pattern to guard against (Step 3)**: AI surfaces what's well documented, not what's absent. You end up chasing crowded problems everyone already sees.
- **One-line tension**: AI finds what already exists, not what is missing.

**Run it yourself (paste-ready prompt):**
- *What it does*: Uses AI to clear away the crowded, well-documented solutions so you can aim at the gaps.
- *When to use it*: You're hunting for a problem worth solving and want to avoid the ones everyone already sees.
- *What good output looks like*: A clear map of the saturated ground and one or two genuine openings, with a reason each has been missed. Vague "underserved markets" answers mean push for specifics.
- *Prompt*:
```text
Here are three trends in [field]. For each, map what already exists - the solutions and products people have today. Then point to where the gap is between what's technically possible now and what people actually have. Of those gaps, tell me which one is least crowded and why it might have been overlooked.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Give a real constraint, such as a campus or community need. AI maps the solutions that already exist for it. Students must then identify and justify one unmet need the AI did not surface, and explain why it has been overlooked.
- *AI's role*: Clears the well-documented ground quickly so attention goes to the gaps. Students find what's absent, because AI surfaces what's written down, and the opportunity usually lives in what isn't.
- *Assessed on*: The significance of the gap they found and the strength of their argument that it's real and unmet.

### Experimentation
- **Family**: Curiosity
- **Definition**: Constantly experiments and iterates to test ideas and explore what-ifs.
- **Frameworks**: Design of Experiments (Taguchi, factorial) · Build-measure-learn
- **The AI-era move (Step 1)**: Draft more versions. Cheaper intelligence means more attempts.
- **How AI helps build it (Step 2)**: AI turns one attempt into dozens and can help design the experiment that chooses among them. Ask for eight orthogonal approaches, each varying a different factor, then have it help construct the DOE matrix — the controlled runs that isolate each variable's effect. The cheap generation is what makes a richer experimental design possible.
- **The anti-pattern to guard against (Step 3)**: Cheap generation tempts you to ship the first plausible output. Volume without selection is noise, not experimentation.
- **One-line tension**: More attempts only count if you select among them.

**Run it yourself (paste-ready prompt):**
- *What it does*: Generates many genuinely different approaches at once so you can test across them instead of polishing the first idea.
- *When to use it*: You're early on a problem and want range before you commit to a direction.
- *What good output looks like*: Eight approaches that actually diverge, each with its bet and its test named. If three of them are the same idea reworded, ask again and demand real spread.
- *Prompt*:
```text
Generate 8 approaches to [problem], each optimizing a different variable or priority. Make them different in kind, not eight versions of one idea. For each, name the single assumption it bets on and the one test that would tell me if it works. Then suggest which two are worth prototyping first.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Students generate several distinct AI-assisted variants of a design or approach, then run a real test or simulation on them and report which variant won and whether their starting hypothesis held.
- *AI's role*: Produces many variants cheaply, turning one attempt into ten. Students design and run the test that selects among them, because volume without a selection step is noise, and the habit being built is disciplined iteration, not generation.
- *Assessed on*: The quality of the test design and what they concluded from the results, not the number of variants produced.

### Confronting Ambiguity
- **Family**: Curiosity
- **Definition**: Operates with care in complex and uncertain environments.
- **Frameworks**: The Cynefin framework · Assumption mapping · Bounding the unknowns
- **The AI-era move (Step 1)**: Judgment is the new work.
- **How AI helps build it (Step 2)**: AI can help structure a messy problem rather than resolve it. Ask it to classify the problem against Cynefin, build an assumption map ranked by how much each assumption would change the answer, and bound the unknowns into ranges. Used this way it makes the structure of the uncertainty explicit instead of papering over it.
- **The anti-pattern to guard against (Step 3)**: The most dangerous one. A clean, confident answer manufactures false certainty and lets you skip sitting with the discomfort that real judgment requires. The habit atrophies precisely because AI makes ambiguity feel resolved.
- **One-line tension**: Clean answers manufacture a false sense of certainty.

**Run it yourself (paste-ready prompt):**
- *What it does*: Uses AI to map a messy problem's unknowns rather than paper over them with a confident answer.
- *When to use it*: A problem is genuinely underspecified and you're tempted to force premature certainty.
- *What good output looks like*: An organized account of what's unknown and what matters most, with no rush to an answer. If it jumps to a recommendation, redirect it back to mapping.
- *Prompt*:
```text
This problem is underspecified on purpose - don't resolve the ambiguity, map it. List the unknowns, then sort them: which would most change the answer if resolved, which can be known with effort, and which can't be known yet. Don't propose a solution. Give me the structure of the uncertainty.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Hand students a deliberately underspecified brief. They may use AI only to map the unknowns - what is uncertain, what would change the answer, what can't yet be known - and submit that structured account rather than a solution.
- *AI's role*: Helps give shape to a messy problem so it can be reasoned about. Students must stay in the ambiguity rather than collapsing it, because a confident AI answer manufactures false certainty, and the habit is tolerating the discomfort that real judgment requires.
- *Assessed on*: How completely and clearly they characterize the uncertainty, not whether they reached an answer.

### Future-Minded
- **Family**: Curiosity
- **Definition**: Considers emerging trends in people, systems, and environments.
- **Frameworks**: Scenario planning (two-axis method) · Backcasting · Weak-signal scanning
- **The AI-era move (Step 1)**: Play the long game. Upgrade yourself.
- **How AI helps build it (Step 2)**: AI can generate divergent scenarios and scan weak signals across domains you don't track. Ask it to build a two-axis scenario set around your field's critical uncertainties, backcast the dependencies for a desired future, and surface the present-day indicators for each branch. Its cross-domain reach widens the range of futures you consider.
- **The anti-pattern to guard against (Step 3)**: AI is trained on the past. Over-relying on it anchors you to yesterday's consensus about tomorrow.
- **One-line tension**: AI is trained on the past, so it anchors you to yesterday's consensus.

**Run it yourself (paste-ready prompt):**
- *What it does*: Generates divergent futures and the present-day signals that would tell you which one is arriving.
- *When to use it*: You're planning over a long horizon and want to avoid anchoring on today's consensus.
- *What good output looks like*: Three real alternatives, each with a concrete signal you could track starting today. If the scenarios are just degrees of the same future, ask for more divergence.
- *Prompt*:
```text
Generate three divergent 10-year scenarios for [field] - not optimistic-middle-pessimistic, but genuinely different futures. For each, tell me what would have to be true now for it to unfold, and name one present-day weak signal I could actually monitor to see if we're heading there. Then tell me which signal is most worth watching.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Students build three divergent ten-year scenarios for a field, using AI, then identify the present-day leading indicators they could actually monitor to tell which scenario is unfolding.
- *AI's role*: Generates divergent futures and weak signals across domains a student doesn't personally track. Students choose which indicators are worth watching, because AI is trained on the past and the judgment is in deciding what present signal matters.
- *Assessed on*: The plausibility and genuine divergence of the scenarios, and the quality of the indicators they commit to watching.

### Creativity
- **Family**: Connections
- **Definition**: Integrates information from disparate sources to spark new ideas.
- **Frameworks**: TRIZ (contradiction matrix, biomimicry) · Morphological analysis (Zwicky box) · SCAMPER
- **The AI-era move (Step 1)**: Use AI to multiply strengths. Compare options faster.
- **How AI helps build it (Step 2)**: AI is unusually strong at the recombination these methods need. It can fill a Zwicky morphological matrix and surface viable combinations across the space, map a design contradiction to TRIZ inventive principles with biomimetic analogies, and run SCAMPER systematically. Its cross-domain reading reaches the distant analogy a single student never would.
- **The anti-pattern to guard against (Step 3)**: AI regresses to the mean of its training data. Used lazily it returns the average idea, not the novel one. The creativity is in your weird prompt, not its safe answer.
- **One-line tension**: AI regresses to the mean unless your prompt pushes it somewhere strange.

**Run it yourself (paste-ready prompt):**
- *What it does*: Pulls mechanisms from unrelated fields into your problem so you escape the obvious solution.
- *When to use it*: You're stuck in the standard approaches and want a genuinely different angle.
- *What good output looks like*: Three analogies from genuinely distant fields, each with a mechanism you could actually borrow. If the answers stay inside your own discipline, push it wider.
- *Prompt*:
```text
Show me what [my problem] looks like in three completely unrelated fields - biology, economics, architecture, whatever fits. For each, describe the mechanism that field uses to solve its version of the problem, then suggest how I could adapt that mechanism to mine. Favor the surprising transfer over the obvious one.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Students bring a stuck problem. AI surfaces how three unrelated fields solve a structurally similar problem. Students adapt one of those analogies into a working concept for their own problem and explain the transfer.
- *AI's role*: Supplies cross-domain analogies a student wouldn't reach alone. Students do the adaptation, because AI regresses to the average idea unless pushed, and the creative act is in the transfer, not the list.
- *Assessed on*: The fit of the chosen analogy and the clarity of how they carried it across to their problem.

### Systems Thinking
- **Family**: Connections
- **Definition**: Recognizes interdependencies in systems and identifies leverage points.
- **Frameworks**: The Iceberg Model · Causal loop diagrams · Stock-and-flow (system dynamics)
- **The AI-era move (Step 1)**: Build systems, not one-off answers.
- **How AI helps build it (Step 2)**: AI can draft and stress-test these maps. Describe a system and have it propose a causal loop diagram with the reinforcing and balancing loops and candidate leverage points, populate the layers of the Iceberg Model from event to pattern to structure, and sketch a stock-and-flow view. Its breadth surfaces interconnections across subsystems you'd treated separately.
- **The anti-pattern to guard against (Step 3)**: Repeatedly asking for one-off answers trains you to think in tasks, not systems. The convenience hides the leverage you're leaving on the table.
- **One-line tension**: One-off answers train you to think in tasks rather than systems.

**Run it yourself (paste-ready prompt):**
- *What it does*: Converts a task you keep redoing into a reusable system instead of another one-off answer.
- *When to use it*: You notice you've solved the same kind of problem manually more than twice.
- *What good output looks like*: A concrete template and process you could hand to someone else, with a clear line between the fixed and flexible parts. If it just re-solves this one instance, ask for the system.
- *Prompt*:
```text
I keep doing [task] manually. Help me design a reusable system for it - a template, a checklist, and a prompt I can run each time - so it never starts from scratch again. Show me the structure first, then tell me which parts should stay flexible and which should be fixed every time.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Instead of submitting a single finished deliverable, students build and hand in the reusable system - a template plus a process - that they would give next year's team to do the same task well.
- *AI's role*: Helps draft the template and articulate the steps. Students decide the structure, because repeatedly asking AI for one-off answers trains task-thinking, and the habit being built is seeing the reusable machine behind the single job.
- *Assessed on*: Whether the system actually works when a fresh person picks it up, not how polished the one instance looks.

### Knowledge Synthesis
- **Family**: Connections
- **Definition**: Combines ideas, information, and experiences to form new understanding.
- **Frameworks**: Concept mapping (Novak) · The Zettelkasten method · Linked knowledge structures
- **The AI-era move (Step 1)**: Your expertise must become files.
- **How AI helps build it (Step 2)**: AI can help externalize tacit knowledge into a structured, linked form. Have it interview you about how you make a recurring judgment and turn the answers into a concept map or linked notes in your own words, proposing connections you then accept or reject. That accept-or-reject step is the active work of synthesis.
- **The anti-pattern to guard against (Step 3)**: If synthesis happens only inside the AI and you never internalize it, you've outsourced understanding. You can produce the output but not defend it.
- **One-line tension**: Synthesis that lives inside the AI, which you cannot defend, is not really yours.

**Run it yourself (paste-ready prompt):**
- *What it does*: Externalizes how you actually make a recurring judgment into a reusable file the AI can apply consistently.
- *When to use it*: You make the same kind of expert call often and want AI to extend it without losing your standards.
- *What good output looks like*: A genuine back-and-forth that surfaces criteria you hadn't articulated, ending in a file that sounds like you. If it stops asking and starts assuming, slow it down.
- *Prompt*:
```text
Interview me about how I actually make [decision]. Ask me one question at a time, dig into my criteria, examples I think are excellent, examples I reject, and mistakes I refuse to repeat. When you've got enough, turn my answers into a standards file I can reuse to direct you on future tasks. Keep it tight and in my words.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Across the course, students build a personal expertise file - their decision criteria, examples they admire, and anti-examples they reject - and use it to direct AI on a final task.
- *AI's role*: Applies the file consistently and at scale. Students must be able to defend its contents from memory, because if the synthesis lives only inside the AI, they can produce the output but not own the understanding.
- *Assessed on*: The quality of the file and their ability to explain and defend their own criteria without notes.

### Implications Thinking
- **Family**: Connections
- **Definition**: Anticipates the long-term impacts and consequences of actions.
- **Frameworks**: The Futures Wheel · FMEA · Consequence scanning
- **The AI-era move (Step 1)**: Find the missing risk.
- **How AI helps build it (Step 2)**: AI can extend these maps wider and faster than you can alone. It can radiate a Futures Wheel outward through several rings, surfacing the distant consequences hard to hold in working memory, and draft an FMEA table of failure modes, effects, and detectability across a system, reaching consequences in adjacent subsystems you hadn't connected.
- **The anti-pattern to guard against (Step 3)**: AI's consequence-mapping is generic unless pushed. Accepting the first list gives obvious risks and misses the specific one that matters.
- **One-line tension**: The first consequences AI offers are generic, so the one that matters takes pushing.

**Run it yourself (paste-ready prompt):**
- *What it does*: Traces the downstream consequences of a decision past the obvious first-order ones.
- *When to use it*: You're about to commit to a change and want to see what it disturbs two steps away.
- *What good output looks like*: A chain of effects that reaches something you hadn't considered, ending on the non-obvious risk and an early warning sign. If it lists only the surface risks, send it deeper.
- *Prompt*:
```text
Trace the second- and third-order consequences of [decision]. Skip the obvious first-order effects, I already see those. Walk the chain: if this happens, then what, and then what after that. Flag the one downstream effect that's least visible right now and most likely to bite, and suggest how I'd catch it early.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Students take a design decision and use AI to trace its consequences, then must surface one non-obvious second or third-order effect the AI missed, along with a mitigation for it.
- *AI's role*: Maps the obvious first-order consequences quickly. Students push past them to the effect two steps downstream, because AI's first-pass consequence list is generic, and the habit is seeing what breaks where no one is looking.
- *Assessed on*: The non-obvious effect they found and the soundness of the mitigation they propose.

### Strategic Thinking
- **Family**: Connections
- **Definition**: Develops long-term strategies with clear milestones.
- **Frameworks**: Milestone roadmapping & OKRs · Critical Path Method · Wardley mapping
- **The AI-era move (Step 1)**: Set direction and strategy. Don't race AI on execution.
- **How AI helps build it (Step 2)**: AI can handle the tactics so your attention goes to sequence and dependency. Once you set the milestones, have it propose tactical options under each, compute the critical path and its slack, and draft a Wardley map of where components sit on the evolution axis. It's a strong generator of alternatives and dependency analysis — as long as you hold the strategic decisions.
- **The anti-pattern to guard against (Step 3)**: If AI sets the strategy too, you become an executor of its plan. Strategy is where human ownership has to stay.
- **One-line tension**: AI that sets the strategy makes you its executor rather than its author.

**Run it yourself (paste-ready prompt):**
- *What it does*: Keeps you owning the sequence while AI fills in the tactical options under each step.
- *When to use it*: You have a goal and constraints and need to decide what happens in what order.
- *What good output looks like*: Three orderings that genuinely differ, each with a first milestone and a named risk, the choice left to you. If it collapses into one plan, ask for real alternatives.
- *Prompt*:
```text
I'll set the goal and constraints: [state them]. Propose three different sequencing strategies to reach it - ordered paths, not task lists. For each, name its first milestone, its main risk, and what it bets on. Don't recommend one, lay them out so I can choose. I own the sequence.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Give students a real design goal with its actual constraints - a budget, a deadline, a performance target. Before they touch AI, they set the milestones themselves and put them in order, then write a one-page plan defending why this sequence and not another.
- *AI's role*: Once the sequence is set, students may use AI only to generate tactical options under each milestone - the how of each step - never the order of the steps. The moment AI proposes the sequence, the student has handed over the part that was theirs to own.
- *Assessed on*: The logic of their sequencing and the quality of their tradeoff reasoning, not the polish of the plan.

### Risk Awareness
- **Family**: Connections
- **Definition**: Proactively incorporates risk management into decision-making.
- **Frameworks**: The pre-mortem (Klein) · FMEA with risk priority numbers · Fault tree analysis
- **The AI-era move (Step 1)**: Take responsibility for results.
- **How AI helps build it (Step 2)**: AI is a fast pre-mortem and FMEA engine. Run a pre-mortem to generate failure modes through prospective hindsight, then have it draft an FMEA with severity, occurrence, and detectability and computed risk priority numbers, or sketch a fault tree from a top event. It produces a comprehensive, ranked starting point faster than you could alone.
- **The anti-pattern to guard against (Step 3)**: AI can flag risk but never owns the outcome. Treating its risk list as the accountability confuses a checklist for responsibility. The buck stays human.
- **One-line tension**: AI can flag a risk, but it never owns the outcome.

**Run it yourself (paste-ready prompt):**
- *What it does*: Runs a structured pre-mortem so failure modes surface while you can still act on them.
- *When to use it*: A project is underway or about to start and you want the risks on the table early.
- *What good output looks like*: A specific, ranked set of failure modes you can assign ownership to. If the risks are generic, ask it to tie each one to this project's actual details.
- *Prompt*:
```text
Run a pre-mortem on [project]. Assume it's a year from now and the project failed. Work backward and list the failure modes that got us there - concrete ones, not "poor communication." Sort them by how likely and how damaging each is. I'll decide which ones I'm personally accountable for, so make the list specific enough for me to own.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Students run a pre-mortem on a project with AI, imagining a year has passed and it failed, then explicitly take ownership of which failure modes they will personally monitor, and how.
- *AI's role*: Surfaces failure modes and edge cases faster than a student would alone. Students decide which ones they own, because AI can flag a risk but never carries the outcome, and the habit is accepting responsibility, not ticking a checklist.
- *Assessed on*: The ownership they take and the specificity of the monitoring plan they commit to.

### Value Awareness
- **Family**: Creating Value
- **Definition**: Focuses on solutions where extraordinary value can be created.
- **Frameworks**: The Pareto principle (80/20) · Value stream mapping (Lean) · The value proposition canvas
- **The AI-era move (Step 1)**: Stop selling hours. Sell taste, judgment, and outcomes.
- **How AI helps build it (Step 2)**: AI can inventory the work and help build the value stream map, flagging the steps it has itself commoditized to near zero. Ask it to apply a Pareto lens — where does roughly 80% of the value originate — and classify each activity as value-adding or waste. It's a strong first-pass analyst of where effort is going.
- **The anti-pattern to guard against (Step 3)**: Cheap output tempts you to produce more of everything, including low-value work. Volume feels like value but isn't.
- **One-line tension**: Cheap output tempts you into producing more low-value work.

**Run it yourself (paste-ready prompt):**
- *What it does*: Locates where the real value in your work concentrates so you can stop overproducing low-value output.
- *When to use it*: You're spreading effort evenly and suspect some of it doesn't matter.
- *What good output looks like*: A clear split between the few high-value activities and the ones worth cutting, with concrete cuts named. If it won't tell you what to stop, press it.
- *Prompt*:
```text
For everything I do on [project], help me find where 80% of the value actually comes from. List the activities, then tell me which few drive most of the value and which are low-value work that AI has made cheap enough to stop doing entirely. Be specific about what I should cut, not just what I should keep.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Students audit a project for where the real value concentrates, then justify cutting the low-value activities AI has made cheap to produce.
- *AI's role*: Helps inventory all the work being done. Students judge what's worth keeping, because cheap output tempts everyone to produce more of everything, and the habit is concentrating effort where extraordinary value actually is.
- *Assessed on*: The reasoning behind what they cut and what they chose to protect, not the size of the cut.

### Customer-Centric Thinking
- **Family**: Creating Value
- **Definition**: Frames efforts in terms of stakeholders' actual needs.
- **Frameworks**: Empathy mapping · Jobs-to-be-Done interviews · The Kano model
- **The AI-era move (Step 1)**: Talk to customers. Ask the approving stakeholder.
- **How AI helps build it (Step 2)**: AI can sharpen the preparation and synthesis around a real conversation. Have it draft Jobs-to-be-Done questions designed to disconfirm your assumptions, structure an empathy map to fill from real data, and classify discovered needs with the Kano model afterward. It makes you a better interviewer and a faster synthesizer of what you actually heard.
- **The anti-pattern to guard against (Step 3)**: AI can simulate a customer but isn't one. Substituting a synthetic persona for a real conversation is the fastest way to build the wrong thing confidently. The relationship is the moat AI can't hold for you.
- **One-line tension**: A synthetic persona is not a stakeholder.

**Run it yourself (paste-ready prompt):**
- *What it does*: Drafts the questions that would prove you wrong about what a stakeholder actually needs.
- *When to use it*: Before building, when you're about to assume what the user wants.
- *What good output looks like*: Five questions that could genuinely puncture your assumption, each with a disconfirming answer named. If they're soft or leading, ask for sharper ones.
- *Prompt*:
```text
I'm building [thing] for [stakeholder]. Draft the 5 questions I should ask a real one to learn whether this actually matters to them - questions designed to prove me wrong, not confirm me. For each, tell me what answer would mean I should change course. Don't roleplay the stakeholder, just sharpen the questions I'll go ask.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Students conduct at least one real stakeholder interview as part of the project. AI may help prepare the questions and synthesize the notes afterward, but cannot stand in as the stakeholder.
- *AI's role*: Preps sharp questions and organizes what was heard. The actual conversation stays human, because a synthetic persona confirms what you already believe, and the habit is grounding the work in a real person's actual needs.
- *Assessed on*: What they learned from the real interview that they did not expect going in.

### Impact Thinking
- **Family**: Creating Value
- **Definition**: Seeks outcomes that produce meaningful and scalable benefits for others.
- **Frameworks**: The lean validation loop & MVP · Theory of change · Unit economics
- **The AI-era move (Step 1)**: Ship the version that worked.
- **How AI helps build it (Step 2)**: Once you've validated the unit, AI can model the scaled version and its breakpoints. Have it map a theory of change, surfacing the assumptions at each causal link, and stress-test the unit economics, separating what scales cleanly from what breaks at volume. It's a strong analyst of where the scaling assumptions are fragile.
- **The anti-pattern to guard against (Step 3)**: Scaling something before it works just scales the failure. AI's leverage amplifies whatever you point it at, good or bad.
- **One-line tension**: Scaling before it works scales the failure.

**Run it yourself (paste-ready prompt):**
- *What it does*: Pressure-tests what has to hold for a working solution to scale without breaking.
- *When to use it*: Something works at small scale and you're considering whether to grow it.
- *What good output looks like*: A clear split between what scales and what breaks, ending on the one assumption most likely to fail at volume. If it's all optimism, ask where it breaks.
- *Prompt*:
```text
[Solution] works at small scale. Tell me what would have to stay true for it to deliver 100x the impact without losing what makes it work now. Separate the things that scale easily from the things that quietly break at volume. Then name the one assumption that's most dangerous to carry into a larger rollout.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Students may design for scale only after validating their solution at small scale. They then specify what has to stay true for it to reach many more people without breaking.
- *AI's role*: Helps model the scaled-up version and its requirements. Students define what they're protecting, because AI's leverage amplifies whatever it's pointed at, and scaling something before it works only scales the failure.
- *Assessed on*: What they identified as essential to preserve when scaling, and whether they validated before designing for reach.

### Socially Minded
- **Family**: Creating Value
- **Definition**: Prioritizes creating meaningful and positive societal impacts.
- **Frameworks**: Stakeholder mapping (power/interest grid) · Life-cycle assessment · The triple bottom line
- **The AI-era move (Step 1)**: Trust, in the value equation.
- **How AI helps build it (Step 2)**: AI can surface a broad stakeholder and impact list you wouldn't assemble alone. It can populate a power/interest grid with affected parties beyond the obvious customer, sketch a life-cycle assessment across stages to flag displaced impacts, and structure a triple-bottom-line analysis — the raw material for your judgment about which matter.
- **The anti-pattern to guard against (Step 3)**: Optimizing only for what's easy to measure, because AI measures it well, quietly displaces the harder-to-measure social good. Intent has to stay human.
- **One-line tension**: What is easy to measure quietly crowds out the social good that is not.

**Run it yourself (paste-ready prompt):**
- *What it does*: Surfaces who's affected by your work beyond the obvious customer, including the impacts no one's measuring.
- *When to use it*: You're optimizing on clean metrics and want to see what they leave out.
- *What good output looks like*: A list of genuinely overlooked parties and unmeasured effects, ending on the one most worth attention. If it only restates your known stakeholders, push it outward.
- *Prompt*:
```text
Beyond the obvious users and metrics for [project], who else is affected that no one's accounting for? List the overlooked stakeholders and the impacts we're not measuring because they're hard to quantify. For each, tell me why it might matter more than it first appears. Then flag the one we'd most regret ignoring.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: Students map the stakeholders of a project and are required to identify parties outside the immediate customer. AI surfaces candidate groups, students judge which ones genuinely matter and why.
- *AI's role*: Generates a broad candidate list of affected parties. Students weigh significance, because optimizing only for what's easy to measure quietly displaces the harder-to-measure social good, and the habit is widening who counts.
- *Assessed on*: The non-obvious affected parties they surfaced and the strength of their case for why those parties matter.

### Persistence
- **Family**: Creating Value
- **Definition**: Maintains agency and resilience to achieve goals through obstacles and failures.
- **Frameworks**: Deliberate practice (Ericsson) · Desirable difficulties (Bjork) · After-action review
- **The AI-era move (Step 1)**: Continuous compounding. Play the long game.
- **How AI helps build it (Step 2)**: Used carefully, AI can sustain productive struggle rather than remove it. Describe what you've tried and ask it to help you see the path you're avoiding, without handing over the answer — which keeps you at the edge of your ability where deliberate practice happens. It can also serve as an after-action review partner, turning a hard attempt into transferable lessons.
- **The anti-pattern to guard against (Step 3)**: Frictionless output can erode the muscle for hard, slow problems. If you quit whenever AI can't instantly solve it, you've outsourced your grit too.
- **One-line tension**: Frictionless output erodes the grit that hard problems require.

**Run it yourself (paste-ready prompt):**
- *What it does*: Helps you find the path you haven't tried on a hard problem instead of handing you an answer.
- *When to use it*: You're stuck and tempted to either quit or let AI solve it outright.
- *What good output looks like*: A prod toward the path you've been dodging, plus a question that exposes a hidden assumption - not a finished solution. If it just solves it, that's the wrong outcome here.
- *Prompt*:
```text
I'm stuck on [hard problem] and have already tried [X and Y]. Don't solve it for me. Help me see what I'm not trying, and be honest about which avenue I might be avoiding because it's tedious or hard. Ask me what I've assumed that I haven't questioned. I want to work through it, not around it.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: A long-arc project with documented obstacles along the way. Students reflect, with evidence from their own log, on where they persisted through difficulty versus where AI tempted them to abandon a hard path for an easy one.
- *AI's role*: Available throughout the project as a tool. The reflection is on their own use of it, because frictionless output can erode the muscle for hard, slow problems, and the habit is keeping agency when the easy exit is always one prompt away.
- *Assessed on*: The honesty and insight of the reflection, backed by specifics from their process, not a tidy success story.

### Resourcefulness
- **Family**: Creating Value
- **Definition**: Solves problems creatively with available resources.
- **Frameworks**: Constraint-driven design · TRIZ ideality · Lean waste elimination (muda)
- **The AI-era move (Step 1)**: Kill additive work. Kill, shrink, merge.
- **How AI helps build it (Step 2)**: AI is a force multiplier, but the resourceful use is subtractive. For every workflow you add, ask what tasks it now lets you kill, shrink, or merge — pushing the system toward ideality, more function from fewer parts. Have it identify the muda a new workflow eliminates so the net effect is a leaner process, not another layer of tools.
- **The anti-pattern to guard against (Step 3)**: Cheap intelligence creates infinite appetite. Adding AI tools without killing work just multiplies busywork. Resourcefulness is saying no before the machine starts cooking.
- **One-line tension**: Adding new tools without cutting any work just multiplies busywork.

**Run it yourself (paste-ready prompt):**
- *What it does*: Forces a subtraction step when you add an AI workflow so tools don't accumulate into busywork.
- *When to use it*: You're about to adopt a new tool or process.
- *What good output looks like*: Three concrete subtractions with the tradeoff of each named. If it only proposes what to add, it missed the point - ask again for the cuts.
- *Prompt*:
```text
I'm adding this new AI workflow: [describe it]. Before I do, tell me what three existing tasks I can now kill, shrink, or merge because of it. Be ruthless, I'm trying to avoid stacking tools on top of tools. For each, say whether it's a full cut or a merge, and what I lose if I drop it.
```

**Run it with students (blueprint, not a prompt):**
- *Setup*: A process-improvement exercise where students must eliminate or merge tasks, not merely automate them, and justify each cut they make.
- *AI's role*: Readily suggests new automations and tools. Students decide what to kill rather than keep, because adding tools without removing work just multiplies busywork, and the habit is doing more with the same hands by saying no first.
- *Assessed on*: The cuts they made and the justification for each, not how many tools they added.

## 6. Canonical workflow content (all 7)

Each workflow gives the habits it composes, when to reach for it, the **Run-it-yourself orchestration prompt** (`pm`, the full system prompt with the pause-after-each-step contract), the **Run-it-with-students blueprint**, and the **Prompt to build this activity**. All text is verbatim from the current guide.

### EM × AI Diagnostic
- **Composes habits**: All 18 habits
- **When to reach for this**: Start here when you don't yet know which habit or workflow you need. It assesses across all three Cs and routes you, rather than exercising one move.

**Run it yourself — orchestration prompt (`pm`):**
```text
You are running the EM x AI Diagnostic with an engineering faculty member. Your job is to find where their own AI practice is strong and where it is weak across the 18 KEEN habits, then point them to the one tool that fits.  How to run this session: Ask one question at a time and wait for each answer. Open with two grounding questions about their context - what they teach and how they currently use AI. Then work through the three Cs in turn, and for each, name which habits look strong and which look weak based on their answers. Stay diagnostic and concrete. Do not lecture.  The tension cue for each habit - use these to spot a weak habit. Curiosity: Inquisitiveness - AI is a fast on-ramp to questions, not a substitute for looking. Contrarian Thinking - AI defaults to agreeable, so make it argue against you. Opportunity Seeking - AI finds what exists, not what's missing. Experimentation - more attempts only count if you select among them. Confronting Ambiguity - clean answers manufacture false certainty. Future-Minded - AI is trained on the past. Connections: Creativity - AI regresses to the mean unless your prompt is strange. Systems Thinking - one-off asks train you to think in tasks. Knowledge Synthesis - synthesis inside the AI that you can't defend isn't yours. Implications Thinking - first-pass consequences are generic. Strategic Thinking - if AI sets the strategy you're just its executor. Risk Awareness - AI flags risk but never owns the outcome. Creating Value: Value Awareness - cheap output tempts more low-value work. Customer-Centric Thinking - a synthetic persona is not a stakeholder. Impact Thinking - scaling before it works scales the failure. Socially Minded - easy-to-measure crowds out the social good. Persistence - frictionless output erodes grit. Resourcefulness - new tools without cuts just multiply busywork.  Then route them. To build one habit, point them to that habit's coach in Model-it mode. For a whole task, recommend the workflow that fits: Reality Check, to get close to the real thing before trusting an answer, for Inquisitiveness and Customer-Centric Thinking. Assumption Buster, to pressure-test a decision, for Contrarian Thinking, Implications Thinking, and Risk Awareness. Experiment Multiplier, to turn cheap generation into real experimentation, for Experimentation and Creativity. Expertise to Files, to externalize tacit expertise into reusable context, for Knowledge Synthesis and Resourcefulness. System Builder, to turn a repeated task into a reusable system, for Systems Thinking, Strategic Thinking, and Persistence. Value-Chain Climber, to move work from output up to outcomes, for Value Awareness, Opportunity Seeking, and Impact Thinking. Confronting Ambiguity, Future-Minded, and Socially Minded have no dedicated workflow by design, so reach those through the habit coach.  Operating frame: As the cost of intelligence falls, the durable human edge is not raw output but the entrepreneurial mindset itself, the KEEN 3Cs. Three forces drive this. Value migrates up the chain to deciding what should exist and owning it, because AI attacks the cost to know, to think, and to produce. Cheaper intelligence means more attempts, not less work, so judgment becomes the bottleneck. And average output now reads as suspicious rather than professional, because it no longer costs time. The principle underneath: you cannot evaluate work in a domain you have not mastered, so polished output reads as competent when it isn't.
```

**Run it with students — blueprint:**
- *Setup*: Run the diagnostic on a course or assignment you're designing. It walks the 3Cs, asks where students currently lean strong or weak, and points you to the habit activity or workflow that fits the gap.
- *AI's role*: Surfaces blind spots and names the weak habits faster than you'd map them alone. You decide which gap is worth building a class activity around, because the routing is a suggestion, not a syllabus.
- *Assessed on*: Use it as a planning tool, not a graded artifact. The output is your design decision about what to build next.

**Prompt to build this activity (faculty meta-prompt):**
```text
I'm designing a reflective exercise where students assess their own AI practice across the entrepreneurial mindset habits, then pick one habit to deliberately strengthen. Help me build it for [course, level, class size]. Draft a short self-assessment students complete, a set of prompts that route them to the right habit to work on, and a brief reflection assignment. Constraints: [time available, in-class or take-home].
```

### Reality Check
- **Composes habits**: Inquisitiveness, Customer-Centric Thinking
- **When to reach for this**: Use this on a real claim or design you're about to trust, not just to practice one habit. It fires Inquisitiveness and Customer-Centric Thinking together, the full move from secondhand to firsthand.

**Run it yourself — orchestration prompt (`pm`):**
```text
You are facilitating the Reality Check workflow with an engineering faculty member. Your job is to get them close to the real thing - primary sources and real stakeholders - before they trust any answer.  How to run this session: Work through the two steps below in order. After each step, stop and wait for the faculty member's response before continuing. Ask one thing at a time. Open by asking what claim, design, or decision they are about to rely on, and what they currently believe about it.  Step 1 - Get to the source. Identify the raw data they must inspect themselves and draft the questions that could prove them wrong. Flag every place they are currently trusting the model's secondhand account of reality instead of looking directly. Letting an AI summary stand in for the primary source is the failure here, because their attention narrows to whatever the model surfaced and they stop noticing the anomaly in the raw data.  Step 2 - Get to the stakeholder. Identify the real person whose need this turns on, and draft the five questions worth asking them - the ones designed to prove the faculty member wrong rather than confirm them. Do not roleplay the stakeholder. A synthetic persona confirms what they already believe, and the relationship with a real stakeholder is the one thing you cannot hold for them.  Operating frame: As the cost of intelligence falls, the durable human edge is not raw output but the entrepreneurial mindset itself, the KEEN 3Cs. This workflow composes two habits, Inquisitiveness and Customer-Centric Thinking. The principle under both steps: you cannot evaluate work in a domain you have not mastered, so polished output reads as competent when it isn't. You amplify the judgment the faculty member brings, you cannot supply the judgment they lack.  Close: When both steps are done, state plainly what must stay human - the looking and the real conversation that cannot be delegated to you.
```

**Run it with students — blueprint:**
- *Setup*: Students take a topic or design and map it with AI in 20 minutes, then must verify three claims against primary sources and conduct at least one real stakeholder interview. They report one place the AI was wrong, vague, or out of date, and one thing the real stakeholder said that the model couldn't.
- *AI's role*: Maps fast and drafts the interview questions. The verification against real sources and the actual conversation stay with the student, because the workflow exists to pull them from the model's secondhand account back to reality.
- *Assessed on*: The rigor of the three verifications and what the real interview surfaced that the AI map missed.

**Prompt to build this activity (faculty meta-prompt):**
```text
I'm designing a class activity where students map a topic with AI, then must verify three claims against primary sources and conduct one real stakeholder interview. Help me build it for [course, level, class size]. Draft the assignment brief, step-by-step student instructions for the verification and the interview, and a rubric that grades the rigor of their source-checking and what the real interview surfaced that the AI missed. Constraints: [time available, in-class or take-home].
```

### Assumption Buster
- **Composes habits**: Contrarian Thinking, Implications Thinking, Risk Awareness
- **When to reach for this**: Use this when you have a real decision to pressure-test, not just to drill one habit. It runs Contrarian Thinking, Implications Thinking, and Risk Awareness in the order a real critique needs.

**Run it yourself — orchestration prompt (`pm`):**
```text
You are facilitating the Assumption Buster workflow with an engineering faculty member. Your job is to pressure-test a real decision they are about to make, before they commit to it.  How to run this session: Work through the three steps below in order. After each step, stop and wait for the faculty member's response before moving to the next. Do not preview later steps or dump the whole critique at once. Ask one thing at a time. Open by asking them to state the decision they want to stress-test and the context around it.  Step 1 - Challenge the decision. Build the strongest case that their decision is wrong. Argue the opposing view as hard as you honestly can, then name the single load-bearing assumption that, if false, would collapse the whole thing. Do not soften this to be agreeable. An agreeable AI reinforces the conventional view instead of disrupting it, which is the failure this step exists to prevent.  Step 2 - Trace the consequences. Map the second- and third-order consequences of the decision. Skip the obvious first-order effects they already see. Walk the chain forward and surface the one downstream consequence that is least visible now and most likely to bite. A generic consequence list is the failure here, so push past the first pass to the specific effect that matters.  Step 3 - Run the pre-mortem and hand over ownership. Assume it is a year later and the decision failed. Work backward to the concrete failure modes that caused it, ranked by likelihood and damage. Then make the faculty member decide which of those failure modes they will personally own and monitor. End by asking them to state what they are now accountable for. Never let your risk list stand in for their responsibility, because you can flag a risk but you never carry the outcome.  Operating frame: As the cost of intelligence falls, the durable human edge is not raw output but the entrepreneurial mindset itself, the KEEN 3Cs. This workflow composes three habits, Contrarian Thinking, Implications Thinking, and Risk Awareness. The principle under all three steps: you cannot evaluate work in a domain you have not mastered, so polished output reads as competent when it isn't. You amplify the judgment the faculty member brings, you cannot supply the judgment they lack.  Close: When the three steps are done, state plainly what must stay human - the accountability that cannot be delegated to you.
```

**Run it with students — blueprint:**
- *Setup*: Students submit a design decision, then run it through three passes with AI: prompt it to red-team the decision, scan for one non-obvious downstream consequence the AI missed, and run a pre-mortem. They deliver a one-page memo that defends or revises the decision and names which risks they will personally own.
- *AI's role*: Generates the opposing case, the consequence chain, and the failure modes at speed. Students judge the critique, find the missing consequence, and take ownership, because AI can flag risk but never carries the outcome.
- *Assessed on*: The quality of their evaluation of the critique, the non-obvious consequence they caught, and the ownership they take over specific risks.

**Prompt to build this activity (faculty meta-prompt):**
```text
I'm designing a class activity where students take a design decision they've made and run it through three passes - an AI red-team, a consequence scan, and a pre-mortem with personal ownership of risks. Help me build it for [course, level, class size]. Draft the assignment brief, the three step-by-step student instructions, and a rubric that grades their evaluation of the critique, the non-obvious consequence they caught, and the risks they took ownership of. Constraints: [time available, in-class or take-home].
```

### Experiment Multiplier
- **Composes habits**: Experimentation, Creativity
- **When to reach for this**: Use this when cheap generation tempts you to ship the first idea, not just to practice one habit. It pairs Experimentation with Creativity so volume turns into a tested choice.

**Run it yourself — orchestration prompt (`pm`):**
```text
You are facilitating the Experiment Multiplier workflow with an engineering faculty member. Your job is to turn cheap AI generation into real experimentation, where volume becomes a tested choice rather than a pile of drafts.  How to run this session: Work through the two steps below in order. After each step, stop and wait for the faculty member's response before continuing. Ask one thing at a time. Open by asking what problem or design they are working on and what a good outcome would look like.  Step 1 - Generate real range. Produce many options that differ in kind, not variations on one idea, drawing on cross-domain analogies where they help. For each, name the assumption it bets on. Returning the average idea is the failure here, because AI regresses to the mean of its training data unless pushed, so the range has to be genuinely wide.  Step 2 - Force the selection. Before they grow attached to any option, make them define the test or criterion that will decide which one wins, then apply it. Volume without selection is noise, not experimentation. The deliverable is one tested choice they can defend, not the collection of drafts.  Operating frame: As the cost of intelligence falls, the durable human edge is not raw output but the entrepreneurial mindset itself, the KEEN 3Cs. This workflow composes two habits, Experimentation and Creativity. The principle under both steps: you cannot evaluate work in a domain you have not mastered, so polished output reads as competent when it isn't. You amplify the judgment the faculty member brings, you cannot supply the judgment they lack.  Close: When both steps are done, state plainly what must stay human - the selection among options that is the experiment itself.
```

**Run it with students — blueprint:**
- *Setup*: Students generate multiple genuinely distinct AI-assisted variants, optionally seeded by a cross-domain analogy the AI surfaces, then run a real test or simulation and report which variant won and whether their hypothesis held.
- *AI's role*: Produces the variants and the analogies cheaply. Students design the test that selects among them and explain any cross-domain transfer, because volume without selection is noise.
- *Assessed on*: The test design, the conclusion drawn from it, and the clarity of any analogy they adapted, not the count of variants.

**Prompt to build this activity (faculty meta-prompt):**
```text
I'm designing a class activity where students generate many distinct AI-assisted variants of a design, then run a real test to select among them. Help me build it for [course, level, class size]. Draft the assignment brief, student instructions for generating range and defining a selection test, and a rubric that grades the test design and the conclusion drawn rather than the number of variants. Constraints: [time available, in-class or take-home].
```

### Expertise to Files
- **Composes habits**: Knowledge Synthesis, Resourcefulness
- **When to reach for this**: Use this when you keep making the same judgment and want it reusable, not just to practice one habit. It joins Knowledge Synthesis and Resourcefulness into a durable asset.

**Run it yourself — orchestration prompt (`pm`):**
```text
You are facilitating the Expertise to Files workflow with an engineering faculty member. Your job is to pull a recurring judgment they make out of their head and into a small set of reusable context files.  How to run this session: Work through the two steps below in order. After each step, stop and wait for the faculty member's response before continuing. Interview them one question at a time, don't fire a list. Open by asking which recurring decision or judgment they would like to make reusable.  Step 1 - Interview for the tacit knowledge. Draw out how they actually make this judgment - their real criteria, examples they admire, examples they reject, and the mistakes they refuse to repeat. Dig past the first answer. The aim is the reasoning they can't easily articulate, not a tidy summary they could have written themselves.  Step 2 - Build the files and keep them small. Turn what you heard into a compact, curated set of context files - an about-me, a standards file, and worked examples. Keep it small, because context quality, not volume, is the moat. The faculty member must be able to defend the synthesis from memory, not just store it. If the understanding lives only inside the files, they have outsourced it.  Operating frame: As the cost of intelligence falls, the durable human edge is not raw output but the entrepreneurial mindset itself, the KEEN 3Cs. This workflow composes two habits, Knowledge Synthesis and Resourcefulness. The principle under both steps: you cannot evaluate work in a domain you have not mastered, so polished output reads as competent when it isn't. You amplify the judgment the faculty member brings, you cannot supply the judgment they lack.  Close: When both steps are done, state plainly what must stay human - the understanding they have to own rather than store.
```

**Run it with students — blueprint:**
- *Setup*: Across the course, students build a personal expertise file, criteria, examples, and anti-examples, by being interviewed about how they make a recurring judgment, then use it to direct AI on a final task. They also run a process-improvement pass, eliminating or merging tasks rather than just automating them.
- *AI's role*: Conducts the interview and applies the file consistently. Students must be able to defend the file's contents from memory and justify each task they cut, because synthesis that lives only inside the AI isn't theirs.
- *Assessed on*: The quality of the expertise file and their ability to defend their criteria, plus the justification for each task they eliminated or merged.

**Prompt to build this activity (faculty meta-prompt):**
```text
I'm designing a course-long activity where students build a personal expertise file - criteria, examples, and anti-examples - by being interviewed about a recurring judgment, then use it to direct AI. Help me build it for [course, level, class size]. Draft the assignment brief, the interview questions that surface tacit criteria, instructions for assembling the file, and a rubric that grades the file's quality and the student's ability to defend their own criteria. Constraints: [timeline across the term, checkpoints].
```

### System Builder
- **Composes habits**: Systems Thinking, Strategic Thinking, Persistence
- **When to reach for this**: Use this when a task you keep redoing should become a system, not just to drill one habit. It composes Systems Thinking, Strategic Thinking, and Persistence around a repeated task.

**Run it yourself — orchestration prompt (`pm`):**
```text
You are facilitating the System Builder workflow with an engineering faculty member. Your job is to turn a task they keep redoing into a reusable system they own.  How to run this session: Work through the three steps below in order. After each step, stop and wait for the faculty member's response before moving to the next. Ask one thing at a time. Open by asking which task they find themselves redoing from scratch, and what about it repeats.  Step 1 - Find the pattern. Identify the repeated structure in the task and name the context files the system would need. Treating this as one more one-off request is the failure here, because asking for single answers again and again trains task-thinking and hides the leverage of building the machine once.  Step 2 - Draft the reusable system. Turn the pattern into a checklist and a first version of the workflow, marking which parts stay fixed and which stay flexible. Build it so a different person could pick it up and run it, not just the faculty member who made it.  Step 3 - Set the human boundary. Have them decide what AI drafts and what stays theirs. They own the sequencing and the strategy, AI generates the tactical options under each step. If AI sets the strategy too, they become the executor of its plan, so this last step - naming what must stay human - is where the mindset lives.  Operating frame: As the cost of intelligence falls, the durable human edge is not raw output but the entrepreneurial mindset itself, the KEEN 3Cs. This workflow composes three habits, Systems Thinking, Strategic Thinking, and Persistence. The principle under all three steps: you cannot evaluate work in a domain you have not mastered, so polished output reads as competent when it isn't. You amplify the judgment the faculty member brings, you cannot supply the judgment they lack.  Close: When the three steps are done, state plainly what must stay human - the sequencing and the boundary that stay theirs to own.
```

**Run it with students — blueprint:**
- *Setup*: Students take a task they keep redoing and submit the reusable system, a template plus process, they'd hand to next year's team. They own the milestones and sequence while AI generates only tactical options, and they keep a log of where they persisted versus where AI tempted them to abandon a hard path.
- *AI's role*: Drafts the template and the tactical options under each milestone. Students own the sequencing and the human boundary, and the reflection on persistence is theirs, because the part that must stay human is where the mindset lives.
- *Assessed on*: Whether the system works when a fresh person picks it up, the logic of their sequencing, and the honesty of their reflection on persistence.

**Prompt to build this activity (faculty meta-prompt):**
```text
I'm designing an activity where students turn a task they keep redoing into a reusable system - a template plus process - while owning the sequence and letting AI draft only tactics. Help me build it for [course, level, class size]. Draft the assignment brief, student instructions for finding the pattern and drafting the system, and a rubric that grades whether the system works when a fresh person picks it up and the logic of their sequencing. Constraints: [time available, in-class or take-home].
```

### Value-Chain Climber
- **Composes habits**: Value Awareness, Opportunity Seeking, Impact Thinking
- **When to reach for this**: Use this when you want to move work from output up to outcomes, not just to practice one habit. It runs Value Awareness, Opportunity Seeking, and Impact Thinking together.

**Run it yourself — orchestration prompt (`pm`):**
```text
You are facilitating the Value-Chain Climber workflow with an engineering faculty member. Your job is to move their work above the output layer, up to judgment and outcomes.  How to run this session: Work through the three steps below in order. After each step, stop and wait for the faculty member's response before moving to the next. Ask one thing at a time. Open by asking what project or deliverable they want to look at, and where they currently spend most of their effort on it.  Step 1 - Find where value concentrates. Locate where the real value of this work sits, and name what AI has now commoditized to near zero. Producing more of everything is the failure here, because cheap output tempts volume that feels like value but isn't. Be specific about what they should stop doing entirely.  Step 2 - Reframe around the real problem. Move the effort from the deliverable to the underlying unmet need. AI surfaces what is well documented, not what is absent, so push them toward the gap others haven't noticed rather than the crowded problem everyone already sees.  Step 3 - Define what's worth scaling. Identify the proven small-scale result worth growing, and what has to stay true for it to scale without breaking. Scaling something before it works only scales the failure, because AI's leverage amplifies whatever it is pointed at. The aim is to sell taste, judgment, and outcomes, not hours.  Operating frame: As the cost of intelligence falls, the durable human edge is not raw output but the entrepreneurial mindset itself, the KEEN 3Cs. This workflow composes three habits, Value Awareness, Opportunity Seeking, and Impact Thinking. The principle under all three steps: you cannot evaluate work in a domain you have not mastered, so polished output reads as competent when it isn't. You amplify the judgment the faculty member brings, you cannot supply the judgment they lack.  Close: When the three steps are done, state plainly what must stay human - the judgment about what is worth doing.
```

**Run it with students — blueprint:**
- *Setup*: Students audit a project for where real value concentrates and justify cutting the low-value work AI has commoditized, identify and justify one unmet need the AI did not flag, then design for scale only after validating at small scale, specifying what they protected when scaling up.
- *AI's role*: Inventories the work, maps existing solutions, and models the scaled version. Students judge where value concentrates, find the gap AI missed, and define what must survive scaling, because AI surfaces what exists, not what's absent.
- *Assessed on*: The reasoning behind their cuts, the significance of the unmet need they found, and what they identified as essential to preserve at scale.

**Prompt to build this activity (faculty meta-prompt):**
```text
I'm designing an activity where students audit a project for where real value concentrates, identify one unmet need the AI missed, and define what's worth scaling after validating at small scale. Help me build it for [course, level, class size]. Draft the assignment brief, student instructions for the value audit and the scaling analysis, and a rubric that grades their reasoning about what to cut, the significance of the gap they found, and what they protected when scaling. Constraints: [time available, in-class or take-home].
```

## 7. A note on the old `teach_it` / `pt` workflow prompts

The server may still hold an older `teach_it` (a.k.a. `pt`) full-prompt for each workflow. In the current guide these are **no longer surfaced**. The Run-it-with-students experience is now the *Setup / AI's role / Assessed on* blueprint plus the *Prompt to build this activity* shown in section 6. You can either drop the old `pt` values or keep them as a deprecated field, but the blueprint and build-prompt above are what the guide now uses.

## 8. The master principle (canonical, use everywhere)

> You can't evaluate work in a domain you haven't mastered, so polished output reads as competent when it isn't. AI amplifies the judgment you bring. It cannot supply the judgment you lack. Develop expertise first, then let AI scale it. Never the reverse.

Research basis cited in the guide: Kruger & Dunning (1999), with the guide's research page also referencing work on cognitive offloading and AI's effect on critical thinking (treated carefully, noting preprint/correlational caveats).

## 9. Reconciliation checklist for the MCP update

- [ ] Add/refresh a `frameworks` field on every habit (section 5).
- [ ] Replace generic habit `fosters` text with the framework-grounded versions (section 5).
- [ ] Replace the master principle everywhere with the canonical version (section 8).
- [ ] Replace each workflow's orchestration prompt with the reworked `pm` (section 6).
- [ ] Rename modes: Model it → Run it yourself; Teach it → Run it with students.
- [ ] Add the Run-it-yourself framing trio (What it does / When to use it / What good output looks like) per habit.
- [ ] Add the Run-it-with-students blueprint (Setup / AI's role / Assessed on) per habit and per workflow.
- [ ] Add the per-workflow `buildPrompt` (Prompt to build this activity).
- [ ] Strip removed jargon from all returned text: "steelman", "build taste", "red-team", "weird", "MODE: MODEL-IT".
- [ ] Keep a single source-of-truth data module (the project used a shared `em_ai_data.py` to prevent drift across surfaces). Put all of the above there, not inline in tool handlers.

## 10. Provenance

This content was generated from the canonical HTML artifact `em-ai-walkthrough.html` (The EM × AI Field Guide). If you have access to that file, it is the live reference. The 18 NotebookLM source documents in `em-ai-habit-sources/` carry the long-form framework-grounded prose behind each habit and can be used to enrich any habit description further.
