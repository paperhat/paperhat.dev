# Copilot Instructions for Paperhat Codex

Use these instructions when working in these Paperhat Codex:

1. Agent
2. Arborist
3. Architect
4. Artificer
5. Auditor
6. Custodian
7. Envoy
8. Exchequer
9. Formulator
10. Linguist
11. Operator
12. Orchestrator
13. Pathfinder
14. Quarrier
15. Quartermaster
16. Reckoner
17. Sentinel
18. Steward
19. Toolsmith
20. Warden

- **Purpose & Architecture**: Pure functional TypeScript/Deno library (monads, branded newtypes, Help system). One function per folder with `index.ts`; no barrel exports. Private helpers live in underscore-prefixed folders/files and are imported with underscores.
- **Workflow**: CLAUDE.md: work sequentially, no batching; after edits run `deno task fmt && deno task lint` unless owners say otherwise. Keep edits small and avoid introducing new lint/type errors.
- **FP Ground Rules**: No classes, mutations, loops, or null. No exceptions—wrap externals into Result/Validation/Help. Functions are curried (exactly one required parameter; no optionals/defaults). Arrow functions allowed only in tests and type positions. Predicates use `is/has/can/should` prefixes. Avoid negation; prefer happy-path positive conditionals.
- **Naming (functions)**: camelCase; CDX components PascalCase. Acronyms are words (`parseXml`), no abbreviations unless on whitelist with `[EXCEPTION]`. Export default on declaration (`export default function padEnd`). Higher-order inner names include outer + preposition + full param (`addToAugend`, `mapWithFunction`). Constructors use legacy names (`just`, `ok`, `help`, `left`, `right`); factories `of/fromX`; transformers `toX` / `fromX` / `xToY`. Aliases allowed in their own folder re-exporting the canonical function. Toolsmith wrapper callbacks may match JS method signatures.
- **Helpers & Placement**: No inline helpers passed to HOFs; extract to underscore folder/file at the lowest common ancestor of consumers. One function per file; HOF outer/inner stay together. No `helpers/` or `utils/` junk drawers.
- **Types**: Use `type`, never `interface` or enums. PascalCase names; acronyms as words; no abbreviations without approval. Prefer descriptive generics. Export on declaration. Types live in `types/index.ts` (LCA); discriminated unions use `_tag` with PascalCase tags. Component props are the exception—export `Props` in the same CDX file.
- **Constants**: No magic values; SCREAMING_SNAKE_CASE names, camelCase object keys. Export on declaration. Constants live in `constants/index.ts` (LCA).
- **Folders & Files**: Function folders camelCase; components PascalCase; private underscore; category folders lowercase single words. In `src/`, all files are `index.*`; tests co-located as `index.test.ts`. `mod.ts` exists only for Envoy module comments, never as a barrel.
- **Imports**: Always include file extensions. Type imports use `import type { Foo } from "..."` (type keyword outside braces). Use aliases (`@paperhat/...`) for public/local exports; relative paths only for private underscore helpers. Never import from barrels. Sort case-sensitively and group per Rule Matrix; add a blank line before code. Re-export aliases with two lines (import then export default).
- **Error & Messaging**: Never throw. Use the Help system with friendly, blame-free language and actionable guidance. Result short-circuits, Validation accumulates, Maybe for optional. Discriminated unions require guards/accessors (`isOk`, `fold`, `getOrElse`); do not reach in or duplicate `_tag` checks. No unreachable code; 100% coverage expected.
- **Newtypes & Guards**: Branded runtime-validated types under `src/newtypes`; construct via smart constructors, validate boundaries with guards, unwrap only through provided helpers.
- **Monads & Effects**: Core monads under `src/monads` (Maybe/Result/Validation/Either/Io/Reader/Writer/etc.). Keep side effects deferred via Io/Future; choose control flow operators consistent with fail-fast vs accumulate vs branch.
- **Testing & Tasks**: `deno task test` (writes coverage/), `test:coverage` for lcov, `killcov` to clean coverage artifacts. `check`/`check:all` for type checks; `fmt`/`fmt:check`; `lint`/`lint:fix`; `dev` or `test:watch` for watch runs.
- **Code Generation**: `.claude/generators` function scaffolding via `deno task new:function <config>` (see .claude/generators/README.md); configs auto-delete unless `--keep`.
- **Docs & Comments**: Use Envoy comments (`//++` or `/*++ */`) to document functions; exceptions tagged `[EXCEPTION] <reason>`. Follow README patterns for map/chain/fold/sequence/traverse/orElse/do-notation and avoid unreachable branches.

If any section is unclear or missing critical project knowledge, please tell me what to adjust or expand.
