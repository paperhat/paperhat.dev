# Work Packet — Scribe Demo 13

## Scope: Default Theme Tokens via DesignPolicy (One-File Theming, Still “Defaults”)

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* DesignPolicy Contract (v0.1) (as applicable)

Inputs:

* Existing default CSS assets from Architect (Demo 10)
* One Codex DesignPolicy document (new) for the demo site, e.g.

  * `paperhat.dev/demo/modules/site/data/design-policy/index.cdx` *(path illustrative; use your module layout rules)*

Outputs:

* The same built pages as Demo 11/12, but with a **site-wide theme applied** by setting tokens
* Deterministic CSS token injection (either a generated `theme.css` linked in `<head>` or an inline `<style>` block)

---

## Objective

Add the smallest possible theming mechanism that preserves the selling point:

> Accept defaults, do almost nothing, get a beautiful complete site.

But also let your partner’s site feel “hers” by editing **one Codex file**.

This packet implements **DesignPolicy as token values only**, not layout logic.

---

## Non-Goals (Explicit)

* Do **not** implement full DesignPolicy language.
* Do **not** implement per-page overrides.
* Do **not** implement component/layout rules, grid systems, etc.
* Do **not** implement multiple themes or theme switching UI.
* Do **not** implement typography engines or CSS generation beyond variables.

Only: a single site-wide token set.

---

## Required DesignPolicy Input (Minimum)

Define a Codex document with one root Concept:

```cdx
<DesignPolicy id="default-site-theme">
	<ThemeTokens>
		<Token name="--ph-font-body" value="system-ui, sans-serif" />
		<Token name="--ph-font-heading" value="system-ui, sans-serif" />
		<Token name="--ph-text-size" value="16px" />
		<Token name="--ph-line-height" value="1.65" />
		<Token name="--ph-content-width" value="72ch" />
		<Token name="--ph-color-text" value="#111111" />
		<Token name="--ph-color-bg" value="#ffffff" />
		<Token name="--ph-color-muted" value="#666666" />
		<Token name="--ph-color-accent" value="#2f6fed" />
		<Token name="--ph-radius" value="10px" />
		<Token name="--ph-space-1" value="0.25rem" />
		<Token name="--ph-space-2" value="0.5rem" />
		<Token name="--ph-space-3" value="1rem" />
		<Token name="--ph-space-4" value="2rem" />
	</ThemeTokens>
</DesignPolicy>
```

Rules:

* Token `name` MUST begin with `--ph-` (Paperhat namespace).
* Token `value` is an opaque string.
* Duplicate token names are an error.

---

## Default CSS Contract (Requirement on Demo 10 assets)

Architect’s default CSS assets MUST reference tokens, not hardcoded values, for:

* fonts
* content width
* base text color / background color
* spacing scale
* accent color

If some hardcoded values exist, it’s acceptable initially, but the goal is token-driven defaults.

---

## Implementation Requirements (Normative)

### 1) Parse + load DesignPolicy

Using the existing Codex parser (Demo 02), parse the DesignPolicy document and extract tokens.

### 2) Emit theme CSS deterministically

Generate a deterministic CSS file content:

```css
:root {
  --ph-font-body: ...;
  ...
}
```

Output location MUST be stable, e.g.:

* `dist/assets/theme.css`

Ordering of declarations MUST be deterministic:

* sort tokens by `name` ascending

### 3) Include theme CSS first

In HTML `<head>`, include the theme CSS **before** all concept CSS assets so concept CSS can use variables:

1. `<link rel="stylesheet" href="/assets/theme.css">`
2. concept-attached assets (deduped, dependency ordered)

### 4) Fail-fast errors

If DesignPolicy parsing fails or tokens invalid:

* build MUST fail deterministically
* no output emitted

### 5) Defaults remain the default

If no DesignPolicy document is present:

* use a built-in default token set (deterministic)
* still emit `theme.css` (or inline) so the mechanism is always present

---

## Required Public API

* `loadThemeTokens(designPolicyPath: string | null): Result<TokenMap, ThemeError[]>`
* `emitThemeCss(tokens: TokenMap): { path: string; css: string }`
* Integrate into the existing site build orchestration (Demo 11/12)

`ThemeError` must include:

* `code`
* `message`
* optional `path`, `line`, `tokenName`

---

## Tests

### A) Token extraction

* Parse the sample DesignPolicy and extract the expected token map.

### B) Deterministic CSS emission

* Emitted CSS is byte-identical across runs.
* Tokens are sorted by name.

### C) Head ordering

* In generated HTML:

  * `theme.css` link appears before all other stylesheet links.

### D) Failure cases

* Duplicate token names → deterministic error
* Token name not starting `--ph-` → deterministic error

### E) No DesignPolicy present

* Build succeeds using built-in defaults and still emits/includes `theme.css`.

---

## Acceptance Criteria

This packet is DONE when:

* The demo site builds with a site-wide theme controlled by one Codex file.
* The mechanism is deterministic, fail-fast, and simple.
* Defaults remain beautiful even without a DesignPolicy file.
* Tests pass.

---

## Notes

* This is the exact kind of “minimal effort customization” that turns defaults into adoption.
* It also sets up later evolution: multiple policies, scoped policies, or richer layout rules—without changing the core demo.
