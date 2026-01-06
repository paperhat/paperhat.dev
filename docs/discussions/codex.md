## 1. What Codex (CDX) _is_

Your canonical formulation (which you explicitly approved and corrected me toward) is:

> **“A declarative semantic language for expressing structured meaning — independent of runtime, presentation, or target platform.”**

Key implications we locked in:

- CDX is **not a web framework**
- CDX is **not markup for HTML**
- CDX is **not tied to JSX, DOMs, browsers, or servers**
- CDX expresses **meaning**, not behavior or layout
- Rendering, persistence, transport, and execution are all _downstream projections_

CDX is closer to:

- a **semantic authoring language**
- a **structural IR for meaning**
- a **human-writable semantic codex**
  than to anything like React, Markdown, or a template engine.

---

## 2. What Paperhat is (post-rename)

Paperhat is the **ecosystem and toolchain** that _uses_ CDX.

Important clarifications we made:

- CDX is **shared across many libraries**
- No single library (including Architect) “owns” CDX
- Paperhat is a **multi-target system**:
  - web
  - static
  - server
  - agent systems
  - data / state / CRDT / pub-sub / commerce / auth

- CDX is the **only interface** app developers use to express:
  - data
  - views
  - configuration
  - policies
  - structure
  - intent

Paperhat is therefore **not**:

- “Paperhat = web framework”
- “Paperhat = renderer”
- “Paperhat = UI library”

It is closer to:

- a **semantic platform**
- a **language-centered system**
- a **codex-driven application environment**

---

## 3. CDX design principles you were adamant about

These came up repeatedly and forcefully:

### a. Minimize cognitive load

- **No extra languages** (no YAML / TOML / TSON)
- No format switching
- One mental model everywhere
- CDX syntax should be learnable once and reused everywhere

### b. Semantic > syntactic

- Concept and trait names must be **plain English**
- Internal IRs may be terse
- Public surface must be obvious and readable
- Names encode meaning, not convenience

### c. Purity and correctness

- If something takes no parameters, it is a **constant**, not a function
- No “pretend purity”
- No mixing impure behavior into semantic declarations
- No lossy semantics hiding behind nice APIs

### d. No accidental complexity

- No duplicate languages
- No copy/paste implementations
- No bloated abstractions
- One function per file
- One concept per module
- Mechanical correctness beats cleverness

---

## 4. CDX vs runtime

We explicitly separated:

- **CDX (semantic declaration)**
  - static
  - analyzable
  - compositional
  - target-agnostic

from:

- **Runtime behavior**
  - lives in renderers, scribes, wardens, reckoners, etc.
  - may be impure
  - may be effectful
  - must _consume_ CDX, not extend it

CDX never:

- fetches data
- mutates state
- performs IO
- encodes timing or execution

It only **describes meaning and structure**.

---

## 5. Contracts and governance

A major theme:

- Every library has a **contract**
- Contracts are:
  - normative
  - locked
  - reviewed
  - enforced mechanically

- Implementation must conform to contract, not the other way around
- Validation is _mechanical_, not interpretive
- “We’ll fix it later” is forbidden

You were especially strict about:

- Validation semantics
- Accumulation correctness
- No ambiguous composition rules
- No “magic” behavior

---

## 6. Your working method (explicitly discussed)

You decided — after real frustration — to:

- Use **this chat** for:
  - architecture
  - language design
  - contracts
  - semantics
  - naming

- Use **other AIs (Copilot / Claude Code)** for:
  - tightly scoped implementation tasks
  - with explicit, narrow instructions
  - no architectural discretion

You asked how prompts should change to reflect this division of labor.

That was a _strategic process decision_, not a throwaway comment.

---

## 7. What I am _not_ assuming

Per your very strong objections in earlier conversations:

- I am **not** assuming:
  - your long-term goals
  - that all chats are part of one master plan
  - that curiosity == commitment

- I am sticking only to things:
  - you stated
  - you corrected me on
  - you explicitly approved

---

## Bottom line

What we established is **not** “a framework”.

It’s this:

> **Paperhat is a language-centered system.
> Codex (CDX) is the semantic language at its core.
> Everything else is a projection, interpreter, or executor of that meaning.**
