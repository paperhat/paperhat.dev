# Envoy Comment Syntax Guide

A comprehensive guide to Envoy's comment syntax that transforms documentation into a living knowledge graph. These aren't just comments - they're structured metadata that powers intelligent documentation!

**CRITICAL:** Envoy **replaces** JSDoc with an entirely different system. DO NOT COPY THE JSDOC VERBOSE STYLE IN ENVOY. They are orthogonal. Envoy understands the code and does not duplicate information in the comments. The code is the single source of truth. Comments are used to add information that cannot be gleaned from the code. They are to be used sparingly.

## 📚 Core Philosophy

**"An Envoy takes what is given"** - The code IS the truth. Comments enhance what machines cannot derive.

### The Automated Documentation Revolution

Envoy's ecosystem (Arborist + Auditor + Quarrier + Envoy) can automatically generate most documentation:

- **Examples**: Quarrier generates property-based test cases that serve as comprehensive examples
- **Gotchas**: Auditor's formal verification discovers edge cases and boundary conditions
- **Pros/Cons**: Envoy analyzes complexity, performance, mathematical properties, and usage patterns
- **Function descriptions**: Often derivable from function names, parameter types, and algorithm analysis

**Manual comments should be the exception, not the rule** - used only for information that machines cannot derive:

- **Business context** that code cannot infer
- **Design decisions** and their rationale
- **Critical issues** requiring human judgment
- **External links** and references
- **Tech debt** with specific remediation plans **but only for _discovered_ tech debt, not as an excuse for creating _new_ tech debt!**

## 🎯 Universal Application

Comments work on ANY code element:

- Functions, constants, types, interfaces, classes, modules, **but in Sitebender, we _never_ use classes or interfaces!**
- Comments must appear DIRECTLY ABOVE what they describe (no blank line for `//++`)
- Multiple Envoy comments can be used throughout the file, but use them sparingly
- If a comment spans more than one line, use the block comment style. Never allow sequential single-line comments

## The Marker System

**CRITICAL:** Single-line comments (`//`) are ONE LINE ONLY. You cannot group multiple `//` lines together. For multi-line content, you MUST use block comments (`/* */`) with the correct Envoy marker (`+`, `-`, `!`, `?`, `>`) operator.

Examples:

```ts
//++ [DESCRIPTION|GROUP|etc.] Single line description comment

/*++
 + [EXCEPTION] Multi-line description comment
 + More discussion
 +
 + [EXPORTS] Use a blank line between usableive comments of the same type
 + (e.g., descriptive)
 */

//?? [EXAMPLE] Example code here

/*??
 ? [EXAMPLE] Multi-line example
 ? With code continuing on sequential lines
 */
```

### 1. Description Marker: `//++`

Describes what ANY code element does.

**PLACEMENT:** IMMEDIATELY ABOVE the code element (no blank line between comment and code). Note: \*\*only the [DESCRIPTION] comment needs to go immediately above the code element. [GROUP] and [END] obviously need to go around what they group. [MODULE] can go at the top of the file (typically, `mod.ts`). As we don't allow barrel files, [MODULE] is typically used with [EXPORTS] to provide links to the actual deep-path exports. [INCLUDES] should go below [EXPORTS] if both are used. [REPLACES] is used in non-module files and should be placed immediately above the descriptive comment (or [EXCEPTION]) in a block descriptive comment immediately above the code element. Example:

```ts
/*++
 + [EXCEPTION] JS OOP methods allowed by explicit permission for performance reasons
 + [REPLACES] This function replaces `===`, e.g., `isEqual(3)(3)`
 + Determines if two arguments are deeply equal
 */
export default function isEqual(a: unknown) { ... }
```

#### Categories for `//++`:

- `[DESCRIPTION]` - Standard description (default if no category specified)
- `[GROUP] Name of group` - Start a group of related elements
- `[END GROUP] Name of group` - End a group, repeat name of group
- `[MODULE]` - Document an entire module/file (use with `/*++ */`)
- `[EXPORTS]` - List public API components (used with MODULE)
- `[INCLUDES]` - List internal/private components (used with MODULE)
- `[REPLACES]` - Give example of what this function replaces, if relevant (e.g., "`isEqual(x)(y)` replaces `x === y`")
- `[EXCEPTION]` - A permitted exception to the rules, typically for optimization (e.g., allowed use of loop)
- `[INVARIANT]` - A condition known to be true that the type system cannot verify; justifies type assertions or unsafe operations

**Functions:**

```typescript
//++ Converts a string to uppercase
export default function toUpperCase(str: string): string {
  return str.toUpperCase();
}
```

**Constants:**

```typescript
//++ Primary brand color for all UI components
export const PRIMARY_COLOR = "#007ACC";

//++ Dark mode background color
export const DARK_BACKGROUND = "#20232A";
```

**Types:**

```typescript
//++ User authentication token with expiry
export type AuthToken = {
  token: string;
  expires: Date;
  refreshToken?: string;
};
```

**Multi-line with Markdown:**

```typescript
/*++
 + # CSV Arborist
 +
 + Parses CSV files with the following features:
 +
 + * Automatic header detection
 + * Unicode support
 + * Configurable delimiters
 */
export default function parseCsv(
  content: string,
): Array<Record<string, string>> {
  // implementation
}
```

### 2. Group Documentation: `[GROUP]` and `[END]`

Groups related code elements with shared documentation.

```typescript
//++ [GROUP] Authentication Constants

//++ JWT signing algorithm
export const JWT_ALGORITHM = "HS256";

//++ Token expiry time in seconds
export const TOKEN_EXPIRY = 3600;

//++ Refresh token expiry (7 days)
export const REFRESH_EXPIRY = 604800;

//++ [END GROUP] Authentication Constants
```

**Nested Groups:**

```typescript
//++ [GROUP] Color System

//++ [GROUP] Brand Colors

//++ Primary interactive color
export const PRIMARY = "#007ACC";

//++ Secondary brand color
export const SECONDARY = "#20232A";

//++ [END GROUP] Brand Colors

//++ [GROUP] Semantic Colors

//++ Usable state color
export const SUCCESS = "#10B981";

//++ Error state color
export const ERROR = "#EF4444";

//++ [END GROUP] Semantic Colors

//++ [END GROUP] Color System
```

### 3. Module Documentation: `[MODULE]`

Documents entire modules (collections of files and folders), not individual files. Used in mod.ts files (NO BARREL FILES!) with EXPORTS/INCLUDES lists because there are NO BARREL FILES.

```typescript
/*++ [MODULE]
 + # Authentication System
 +
 + Comprehensive authentication handling including:
 +
 + ## Features
 +
 + 1. **JWT Token Management**
 +    - Token generation and validation
 +    - Automatic refresh handling
 +    - Secure storage
 +
 + 2. **Session Management**
 +    - Stateless sessions
 +    - Redis-backed persistence
 +    - Automatic cleanup
 +
 + 3. **Permission System**
 +    - Role-based access control (RBAC)
 +    - Fine-grained permissions
 +    - Dynamic policy evaluation
 +
 + ## Security
 +
 + All tokens use **HS256** signing with rotating secrets.
 + Passwords are hashed using **bcrypt** with cost factor 12.
 */
```

**Module References (for superdevs without barrel files):**

```typescript
/*++
 + [MODULE]
 + # Arborist Library
 +
 + Advanced TypeScript parsing and analysis
 +
 + [EXPORTS]
 + ./parse/parseSourceFile
 + ./parse/extractFunctions
 + ./parse/extractTypes
 +
 + [INCLUDES]
 + ./internal/createCompiler
 + ./internal/traverseAST
 + ./internal/symbolTable
 */
```

### 4. Reference/Link Marker: `//>>`

Creates semantic links using HTML `rel` values. Content is markdown link format.

**PLACEMENT:** In the code if it's a direct reference to something specific, or at the bottom of the file as 'see also' references.

**Navigation Links:**

```typescript
/*>>
 > [NEXT] [Session Management](./session/README.md)
 > [PREV] [Getting Started](../mission-control/getting-started.md)
 > [UP] [Authentication Overview](../README.md)
 > [INDEX] [API Reference](../../api/index.md)
 */
```

**Documentation Links:**

```typescript
/*>>
 > [GLOSSARY] [JWT](https://jwt.io/introduction)
 > [HELP] [Troubleshooting Auth](./docs/troubleshooting.md)
 > [CANONICAL] [RFC 7519 - JWT Spec](https://tools.ietf.org/html/rfc7519)
 */
```

**Attribution:**

```typescript
/*>>
 > [AUTHOR] [Guy Beford](https://github.com/guybeford)
 > [LICENSE] [MIT License](./LICENSE)
 > [COPYRIGHT] Copyright 2025 Sitebender
 */
```

**Related Resources:**

```typescript
/*>>
 > [RELATED] [OAuth 2.0 Guide](https://oauth.net/2/)
 > [ALTERNATE] [Legacy Auth Docs (v1)](./legacy/auth-v1.md)
 > [EXTERNAL] [Security Best Practices](https://owasp.org/auth)
 */
```

### 5. Help Marker: `//??`

Provides examples, gotchas, pros/cons, and other helpful info with full markdown support.

**PLACEMENT:** Below the code element with ONE BLANK LINE above and below for visual breathing room.

#### Available Categories:

- `[EXAMPLE]` - Code examples showing usage (default if no category)
- `[GOTCHA]` - Unexpected behavior or common mistakes
- `[HINT]` - Helpful tips or suggestions for related approaches
- `[PRO]` - Benefits or strengths of the function
- `[CON]` - Limitations or weaknesses
- `[SETUP]` - Required setup or configuration
- `[STEP #]` - A single step in the setup (must be used with `[SETUP]`) — # is step number, e.g., `[STEP 2]`
- `[ADVANCED]` - Advanced usage patterns
- `[MIGRATION]` - How to migrate from old versions

````typescript
/*??
 ? [EXAMPLE]
 ? ## Basic Usage
 ?
 ? ```typescript
 ? const token = await generateToken(user)
 ? const valid = await validateToken(token)
 ? ```
 ?
 ? ## With Error Handling
 ?
 ? ```typescript
 ? try {
 ?   const token = await generateToken(user)
 ?   res.cookie('auth', token, { httpOnly: true })
 ? } catch (error) {
 ?   logger.error('Token generation failed', error)
 ? }
 ? ```
 ?
 ? [GOTCHA]
 ? **Warning**: Tokens expire after 1 hour by default.
 ? Set `TOKEN_EXPIRY` environment variable to customize.
 ?
 ? [PRO]
 ? * Stateless authentication
 ? * Works across microservices
 ? * No server-side session storage
 ?
 ? [CON]
 ? * Token size larger than session cookies
 ? * Cannot revoke tokens before expiry
 ? * Requires careful secret management
 */
````

### 6. Tech Debt Marker: `//--`

Documents known issues, workarounds, or areas needing improvement.

**PLACEMENT:** WHERE the tech debt occurs (typically inside functions, right at the problematic code).

**CRITICAL:** WE DO NOT CREATE TECH DEBT. WHEN WE DISCOVER IT WE FIX IT IMMEDIATELY. WE ONLY COMMENT TECH DEBT IF IT CANNOT BE FIXED IMMEDIATELY. NO EXCEPTIONS. THIS COMMENT STYLE IS **NOT** PERMISSION TO CREATE TECH DEBT.

```typescript
/*--
 - [REFACTOR]
 - ## Current Issues
 -
 - 1. Using regex instead of proper AST parsing
 - 2. O(n²) complexity in the main loop
 - 3. No caching of computed results
 -
 - ## Migration Plan
 -
 - - [ ] Replace regex with Arborist library
 - - [ ] Implement memoization
 - - [ ] Add Redis caching layer
 -
 - **Target**: Q1 2025
 */
```

#### Tech Debt Categories:

- `[WORKAROUND]` - Temporary fix for a problem
- `[LIMITATION]` - Known limitation of current approach
- `[OPTIMIZE]` - Performance improvement needed
- `[REFACTOR]` - Code structure needs improvement
- `[COMPATIBILITY]` - Compatibility issue to address

### 7. Critical Issue Marker: `//!!`

Marks critical problems that MUST be fixed. These block releases!

**PLACEMENT:** Next to the specific issue OR if file-wide: below imports, above the description comment and function/component (with blank lines above and below the critical comment for proper visual hierarchy).

````typescript
/*!!
 ! [SECURITY]
 ! # SQL Injection Vulnerability
 !
 ! **Severity**: CRITICAL
 ! **CVE**: Pending
 !
 ! User input is directly interpolated into SQL query.
 !
 ! ## Impact
 ! - Database compromise possible
 ! - User data exposure
 ! - Privilege escalation
 !
 ! ## Fix Required
 ! Replace string interpolation with parameterized queries:
 !
 ! ```typescript
 ! // WRONG
 ! db.query(`SELECT * FROM users WHERE id = ${userId}`)
 !
 ! // CORRECT
 ! db.query('SELECT * FROM users WHERE id = ?', [userId])
 ! ```
 */
````

#### Critical Issue Categories:

- `[SECURITY]` - Security vulnerabilities
- `[PERFORMANCE]` - Severe performance issues
- `[CORRECTNESS]` - Produces wrong results
- `[INCOMPLETE]` - Missing critical functionality
- `[BREAKING]` - Will break in production

## 📋 Complete Example (With Proper Spacing)

**The example below is for information only. We NEVER put multiple function definitions in the same file (unless they are part of one higher-order function).**

````typescript
import { AstNode } from "../types/index.ts";

//!! [INCOMPLETE] Generator function support not implemented

//++ [GROUP] Associativity Detection

//++ Detects if a function exhibits associative behavior
export function isAssociative(node: AstNode): boolean {
  //-- [OPTIMIZE] This recursion should probably be a loop
  return hasBinaryAssociativeOperator(node) || hasAssociativeMethodCall(node);
}

/*??
 ? [EXAMPLE]
 ? ```typescript
 ? const addNode = parse('(a, b) => a + b')
 ? isAssociative(addNode) // true
 ?
 ? const subNode = parse('(a, b) => a - b')
 ? isAssociative(subNode) // false
 ? ```
 ?
 ? [GOTCHA]
 ? Only detects **structural** patterns, not semantic equivalence.
 */

//++ Helper to check for associative operators
function hasBinaryAssociativeOperator(node: AstNode): boolean {
  // implementation
}

//++ [END GROUP] Associativity Detection

//++ [GROUP] Commutativity Detection

//++ Detects if a function exhibits commutative behavior
export function isCommutative(node: AstNode): boolean {
  // implementation
}

//++ [END GROUP] Commutativity Detection

/*>>
 > [RELATED] [Category Theory](https://en.wikipedia.org/wiki/Category_theory)
 > [AUTHOR] [Guy Beford](https://github.com/guybeford)
 */
````

Note the spacing:

- `//!!` file-wide issue has blank lines above and below
- `//++` descriptions are immediately above code (no gap)
- `//??` help has at least one blank line above and below
- `//--` tech debt is right where the issue occurs
- `//>>` references are at the bottom of the file, for reference but not creating noise

## 🎨 Markdown Support Everywhere

All comment content supports:

- **Headings**: `# H1`, `## H2`, `### H3`
- **Lists**: `* bullet`, `- dash`, `1. numbered`
- **Links**: `[text](url)`
- **Images**: `![alt text](path/to/image.png)` or `![diagram](https://example.com/diagram.svg)`
- **Code**: `` `inline` `` and ` ```blocks``` `
- **Emphasis**: `**bold**`, `*italic*`, `~~strikethrough~~`
- **Tables**, blockquotes, and more!

## 📐 Smart Association Rules

1. **Description markers (`//++`)** associate with the NEXT code element (no blank line between)
   - Exception: `[MODULE]` can stand alone to describe the entire module (multiple files/folders)
   - `[EXPORTS]` and `[INCLUDES]` are typically used with `[MODULE]` for superdevs without barrel files (**barrel files are prohibited**)
2. **Help markers (`//??`)** appear below code with at least one blank line for spacing
3. **Tech debt (`//--`)** goes exactly where the issue is in the code
4. **Critical issues (`//!!`)** next to issue or file-wide with proper spacing
5. **Links (`//>>`)** in code for direct refs or at file bottom as references
6. Blank lines and regular comments (`//` without markers) are ignored, do not use regular comments to explain code that should be obvious from the code itself. Keep files terse and readable.
7. Arborist automatically determines element type
8. Orphaned `[END GROUP]` markers are ignored but reported in diagnostics

## ✅ Best Practices

### Automated-First Approach

**PREFER**: Let the system generate documentation automatically

- Quarrier generates comprehensive examples from property-based tests
- Auditor discovers gotchas through formal verification and edge case detection
- Envoy analyzes pros/cons from complexity, performance, and mathematical properties
- Function descriptions often derivable from names, types, and algorithm structure

**USE MANUAL COMMENTS ONLY FOR**:

- Business context machines cannot infer
- Design decisions and rationale
- Critical issues requiring human judgment
- External references and links
- Tech debt with specific remediation plans

### When You Do Comment

#### DO:

- ✅ Use `//++` for the function description (required) — when possible, a terse but clear single-line description (do not include information that can be gleaned from the code itself)
- ✅ Group related constants/types with `//++ [GROUP] Group name` and `//++ [END GROUP] Group name` when logical grouping isn't obvious; put blank lines around each.
- ✅ Add `/*++ [MODULE] ... */` documentation for business context (only in mod.ts IF we use a mod.ts — ask before creating)
- ✅ Use `//!!` for critical issues requiring immediate attention
- ✅ Use `//--` for tech debt with clear remediation plans
- ✅ Use `//>>` for semantic links to external resources
- ✅ Use the comment group symbol (+, -, etc.) for the start of inner lines of multiline comments, aligned with the \*s (see above)

#### DON'T:

- ❌ Add examples manually - let Quarrier generate comprehensive test-based examples
- ❌ Document gotchas manually - let Auditor discover them through formal verification
- ❌ List pros/cons manually - let Envoy analyze and measure them
- ❌ Try to group multiple `//` lines together - use `/* */` blocks instead
- ❌ Use type markers like `[FUNCTION]` - Arborist determines this automatically
- ❌ Mix categories in one line (`//?? [EXAMPLE] [GOTCHA]`)
- ❌ Leave tech debt without reasons
- ❌ Create unmatched `[GROUP] Name of group` without `[END GROUP] Name of group`
- ❌ Use asterisk `*` for block comment margins

## 🔗 Quick Reference (For AIs That Don't Read So Good)

### The Golden Rules

1. **`//` comments are ONE LINE ONLY** - cannot be grouped
2. **Block comments for multi-line** - use `/*++ + */`, `/*?? ? */`, `/*-- - */`, etc. with the marker repeated on each inner line
3. **Description `//++` goes IMMEDIATELY ABOVE the code** (no blank line)
4. **Help `//??` needs breathing room** (at least one blank line above)
5. **Tech debt `//--` goes WHERE the problem is**
6. **Critical `//!!` file-wide issues need spacing** (blank lines above/below)
7. **Links `//>>` go in code or at bottom** as references
8. **Bad syntax = ignored + reported**

### All Markers at a Glance

| Marker | Single Line | Block     | Purpose           | Associates With Code? |
| ------ | ----------- | --------- | ----------------- | --------------------- |
| `//++` | ✅          | `/*++ */` | Describe elements | ✅ (NEXT element)     |
| `//??` | ✅          | `/*?? */` | Help/examples     | ❌ (metadata only)    |
| `//--` | ✅          | `/*-- */` | Tech debt         | ❌ (metadata only)    |
| `//!!` | ✅          | `/*!! */` | Critical issues   | ❌ (metadata only)    |
| `//>>` | ✅          | `/*>> */` | Links/references  | ❌ (metadata only)    |

### Description Categories (`//++`)

| Category        | Usage             | Example                           |
| --------------- | ----------------- | --------------------------------- |
| `[DESCRIPTION]` | Default, optional | `//++ Adds two numbers`           |
| `[GROUP]`       | Start group       | `//++ [GROUP] Math utilities`     |
| `[END GROUP]`   | End group         | `//++ [END GROUP] Math utilities` |
| `[MODULE]`      | Entire module     | `//++ [MODULE] Auth System`       |
| `[EXPORTS]`     | Public API        | `//++ [EXPORTS] ./login`          |
| `[INCLUDES]`    | Internal files    | `//++ [INCLUDES] ./internal/util` |
| `[REPLACES]`    | What it replaces  | `//++ [REPLACES] x === y`         |
| `[EXCEPTION]`   | Permitted exception | `//++ [EXCEPTION] Loop for perf` |
| `[INVARIANT]`   | Type system can't verify | `//++ [INVARIANT] Only Helps remains` |

### Help Categories (`//??`)

| Category      | Purpose                 | Example                                                   |
| ------------- | ----------------------- | --------------------------------------------------------- |
| `[EXAMPLE]`   | Code examples (default) | `//?? [EXAMPLE] add(2, 3) // 5`                           |
| `[GOTCHA]`    | Warnings                | `//?? [GOTCHA] Returns NaN for invalid input`             |
| `[HINT]`      | Tips and suggestions    | `//?? [HINT] To remove falsy values, use filter(Boolean)` |
| `[PRO]`       | Benefits                | `//?? [PRO] Very fast implementation`                     |
| `[CON]`       | Limitations             | `//?? [CON] Only works with integers`                     |
| `[SETUP]`     | Requirements            | `//?? [SETUP] Requires Deno 2.6+`                         |
| `[STEP #]`    | Setup step              | `//?? [STEP 1] Install the latest Deno`                   |
| `[ADVANCED]`  | Complex usage           | `//?? [ADVANCED] Can be curried: add(2)(3)`               |
| `[MIGRATION]` | Version changes         | `//?? [MIGRATION] v2.0 removed the third parameter`       |

### Tech Debt Categories (`//--`)

| Category          | Usage               |
| ----------------- | ------------------- |
| `[WORKAROUND]`    | Temporary fix       |
| `[LIMITATION]`    | Known limitation    |
| `[OPTIMIZE]`      | Performance issue   |
| `[REFACTOR]`      | Structure problem   |
| `[COMPATIBILITY]` | Compatibility issue |

### Critical Issue Categories (`//!!`)

| Category        | Usage                      |
| --------------- | -------------------------- |
| `[SECURITY]`    | Security vulnerability     |
| `[PERFORMANCE]` | Severe performance problem |
| `[CORRECTNESS]` | Wrong results              |
| `[INCOMPLETE]`  | Missing functionality      |
| `[BREAKING]`    | Will break in production   |

### Link Categories (`//>>`)

**Navigation**: `[NEXT]`, `[PREV]`, `[UP]`, `[INDEX]`, `[CONTENTS]`, `[FIRST]`, `[LAST]`
**Documentation**: `[GLOSSARY]`, `[HELP]`, `[APPENDIX]`, `[BOOKMARK]`
**Attribution**: `[AUTHOR]`, `[LICENSE]`, `[COPYRIGHT]`
**Relationships**: `[CANONICAL]`, `[ALTERNATE]`, `[RELATED]`, `[EXTERNAL]`

### Common Mistakes (DON'T DO THESE!)

❌ **WRONG - Trying to group single-line comments:**

```typescript
//++ This is a function
//++ that does something important  // ← WRONG! Will be ignored!
function doSomething() {}
```

✅ **CORRECT - Use block comments for multi-line:**

```typescript
/*++
 + This is a function
 + that does something important
 */
function doSomething() {}
```

❌ **WRONG - Using asterisks in block comments:**

```typescript
/*++
 * Use the same symbol
 * as used in the opening line (+)
 * not the asterisk or pipe
 */
```

✅ **CORRECT - Use the same symbol in block comments:**

```typescript
/*++
 + This works perfectly
 + and supports markdown
 */
```

❌ **WRONG - Missing category brackets:**

```typescript
//?? EXAMPLE add(2, 3) // ← WRONG! No brackets
```

✅ **CORRECT - Always use brackets for categories:**

```typescript
//?? [EXAMPLE] add(2, 3) // 5
```

❌ **WRONG - Multiple categories in one line:**

```typescript
//?? [EXAMPLE] [PRO] add(2, 3) // ← WRONG!
```

✅ **CORRECT - One category per line (single-line categories):**

```typescript
/*??
 ? [EXAMPLE] add(2, 3) // 5
 ? [PRO] Very fast performance
 */
```

✅ **CORRECT - Multi-line categories need blank lines between them:**

````typescript
/*??
 ? [EXAMPLE]
 ? ```typescript
 ? const result = add(2, 3)
 ? console.log(result) // 5
 ? ```
 ?
 ? [GOTCHA]
 ? May return NaN if either argument is not a number.
 ? Always validate inputs before calling.
 */
````

Note: Content starts on the line AFTER the opening `/*??`, not on the same line. No blank line needed immediately after the opening marker or before the closing marker.

### Syntax Patterns for Copy-Paste

**Simple description:**

```typescript
//++ Converts string to uppercase
export function toUpper(str: string): string {
```

**Group of related items:**

```typescript
//++ [GROUP] Color constants

//++ Primary brand color
export const PRIMARY = "#007ACC";

//++ Secondary color
export const SECONDARY = "#666";

//++ [END GROUP] Color constants
```

**Function with help:**

```typescript
//++ Adds two numbers together
export function add(a: number, b: number): number {
  return a + b;
}

/*??
 ? [EXAMPLE] add(2, 3) // 5
 ? [GOTCHA] May return NaN with invalid input
 */
```

**Module documentation:**

```typescript
/*++
 + [MODULE]
 + # Authentication System
 + Handles JWT tokens and sessions
 +
 + [EXPORTS]
 + ./auth/login
 + ./auth/logout
 */
```

## 🚀 The HATEOAS Revolution: Documentation as Living Knowledge Graph

These comments don't just create documentation - they power a **revolutionary transformation** of how we understand and navigate codebases.

### 🧭 ENVOY: The Project Intelligence Platform

**Not just documentation generation, but your codebase's diplomatic representative.**

"An Envoy takes what is given" - No assumptions, no guessing, just pure representation of your code's reality.

### 📊 Five Data Sources Creating the Knowledge Graph

#### 1. **Filesystem Semantics**

Path structure reveals dependencies: `a/b/c` means `c` is used by `b`, `b` is used by `a`. Folder names encode categories. Arborist infers semantic meaning from architectural patterns.

#### 2. **TypeScript Analysis Data**

Full symbol analysis, type relationships, import/export mappings, call graphs, implementation chains via Arborist.

#### 3. **Configuration Files (First-Class Citizens)**

- `deno.jsonc` with inline comment documentation
- `deno.lock` for security tracking
- `.editorconfig` for style guide generation
- Lint/format configs for convention documentation

#### 4. **Git History Integration**

When functions were added/modified, author attribution, tech debt age tracking.

#### 5. **CSS Analysis**

Parse styles, match to components, document theming systems and progressive enhancement layers.

### 🕸️ The Knowledge Graph Structure

**Nodes**: Modules, Functions, Types, Constants, TSX Components, CSS Classes
**Edges**: `imports`, `calls`, `implements`, `uses`, `contains`, `extends`, `styles`, `tests`

**Triple Store Integration** via Apache Jena Fuseki with **SPARQL Query Support**:

```sparql
# What functions call parseSourceFile?
SELECT ?caller WHERE {
  ?caller calls :parseSourceFile
}

# What is the impact radius of changing this function?
SELECT ?affected WHERE {
  :targetFunction <-calls- ?affected
}

# Show me all security vulnerabilities by age
SELECT ?function ?issue ?age WHERE {
  ?function hasIssue ?issue .
  ?issue hasCategory "SECURITY" .
  ?issue hasAge ?age
} ORDER BY DESC(?age)
```

### 🔗 HATEOAS Implementation: Every Page is a State Machine

Each documentation page represents a **navigable state** with hypermedia controls:

```json
{
  "_links": {
    "self": "/functions/parseSourceFile",
    "module": "/modules/arborist",
    "calls": ["/functions/createCompiler", "/functions/readFile"],
    "calledBy": ["/functions/analyze", "/functions/lint"],
    "implements": "/types/arborist",
    "next": "/functions/extractFunctions",
    "tests": ["/tests/parseSourceFile.test.ts"],
    "source": "/src/parseSourceFile/index.ts",
    "author": "/authors/guybeford",
    "lastModified": "2025-09-10T14:30:00Z"
  }
}
```

**Context-Aware Navigation**: Links change based on location, "next steps" vary by entity type, related items highlighted, impact analysis available.

### ⚠️ Architectural Consistency Through Truth

**The Diplomatic Approach**: When conflicts arise, Envoy chooses the code as the single source of truth and politely ignores developer inconsistencies, with friendly warnings to help correct mistakes.

**Import Alias vs Filesystem Conflicts**: When aliases don't match nesting patterns, trust the filesystem structure and report the alias as "Architectural Inconsistency" with suggestions for alignment.

**Comment Category Misuse**: If someone uses `[EXPORTS]` in a function description instead of with `[MODULE]`, treat it as a regular description and warn about proper usage.

**API Boundary Violations**: When internal functions are imported externally, note the violation and suggest either making it officially public or stopping the import.

**Bad Comment Syntax**: Single-line comments grouped together are simply ignored, with helpful reminders about using block comments for multi-line content.

**Version Change Tracking**: Generate changelogs from `deno.jsonc` export changes and conventional commits, noting any inconsistencies.

### 🎯 Core Features

1. **Graph Construction**
   - Filesystem semantic parser, TypeScript symbol analysis, dependency extraction, HATEOAS state/transitions

2. **Triple Store Integration**
   - Apache Jena Fuseki backend, RDF triple generation, SPARQL query interface

3. **Comprehensive Dashboard**
   - Critical bugs aggregated, tech debt by age, test coverage gaps, complexity hotspots, recent changes, author contributions, linting status, formatting compliance, versioning overview

4. **Intelligent Navigation**
   - Context-aware links, impact analysis, dependency trees, call flow tracking

5. **Multi-Source Metadata**
   - From filesystem paths, config files, git history, TypeScript analysis via Arborist

### 🚀 Interactive Features

1. **Live Playgrounds**
   - **Functions**: Editable parameters with real-time results
   - **Components**: Rendered output with props editor
   - **Types**: Example data validation
   - **CSS**: Theme switcher and live editing

2. **Progressive Enhancement Viewer**
   - Toggle: HTML only / HTML+CSS / HTML+CSS+JS
   - Shows degradation strategy, side-by-side comparison

3. **Visual Graph Explorer**
   - D3-powered dependency trees, call flow diagrams, impact radius heat maps

4. **Advanced Intelligence**
   - API breaking change detection, migration path generation, security audit integration, bundle size tracking

5. **Automated Style Guide Generation**
   - From lint/format configs, convention documentation, code style examples

### 🎭 The Envoy Philosophy

"An Envoy takes what is given" - The system is built on truth:

- Takes the filesystem structure AS IT IS
- Takes the configuration AS WRITTEN
- Takes the code AS IMPLEMENTED
- Reports conflicts HONESTLY
- Maintains architectural CONSISTENCY through diplomatic truth-telling

**No assumptions. No guessing. Just diplomatic representation of reality.**

---

Remember: The code IS the documentation. These comment markers are the diplomatic protocol that transforms your codebase into an intelligent, navigable, queryable knowledge graph that reveals architectural truth and enforces consistency.
