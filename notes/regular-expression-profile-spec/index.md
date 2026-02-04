Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Regular Expression Profile Specification

---

## 1. Purpose

This specification defines the **single canonical regular expression language** used by:

* `MatchesRegularExpression`
* `DoesNotMatchRegularExpression`

The purpose is to guarantee:

* deterministic behavior across all backends
* closed-world, analyzable patterns
* safe and predictable performance
* stable compilation to SHACL constraints and other targets

This profile is intentionally **restricted**.
Engine-specific extensions are forbidden.

---

## 2. Scope

This profile governs:

* the grammar and semantics of regular expression patterns
* which constructs are permitted
* which constructs are forbidden
* how matching is performed
* how patterns interact with Unicode text

This profile does **not** govern:

* locale-aware collation
* normalization (handled separately)
* any runtime flags provided by host regex engines

---

## 3. Core Model

### 3.1 Input text model

* Input text is a sequence of **Unicode scalar values**.
* Pattern matching is performed over scalar values, not bytes.

### 3.2 Matching mode

All matches are performed using **leftmost-first** matching:

* The engine selects the leftmost position in the input at which a match can occur.
* At that position, the engine selects the first match consistent with the pattern structure.

This specification does not require a particular implementation strategy (backtracking, NFA, DFA), but it does require the same observable results.

### 3.3 Full-match vs substring-match

`MatchesRegularExpression(string, pattern)` returns true iff:

* the pattern matches **at least one substring** of `string`

If full-string matching is required, authors MUST use anchors `^` and `$`.

---

## 4. Lexical Structure

### 4.1 Pattern encoding

Patterns are Unicode strings.

### 4.2 Escapes

A backslash introduces an escape sequence.

If an escape sequence is not defined by this specification, the pattern is invalid.

---

## 5. Grammar (Permitted Constructs)

A pattern consists of an alternation of one or more concatenations.

### 5.1 Alternation

* `A|B` matches either `A` or `B`.

### 5.2 Concatenation

* `AB` matches `A` followed by `B`.

### 5.3 Grouping

* `(A)` groups subexpressions for precedence.
* Capturing groups are permitted but **captures are not observable** in this surface.
* Non-capturing groups `(?:A)` are forbidden.

### 5.4 Literals

A literal character matches itself, except for metacharacters.

Metacharacters are:

* `\`
* `.`
* `^`
* `$`
* `|`
* `(`
* `)`
* `[`
* `]`
* `*`
* `+`
* `?`
* `{`
* `}`

To match a metacharacter literally, it MUST be escaped.

### 5.5 Any-character

* `.` matches any single Unicode scalar value **except** line terminators.

Line terminators are:

* `U+000A` LINE FEED
* `U+000D` CARRIAGE RETURN

### 5.6 Anchors

* `^` matches the start of the string.
* `$` matches the end of the string.

Anchors are absolute; there is no multiline mode.

### 5.7 Character classes

Character classes are delimited by `[...]`.

Permitted forms:

* Single characters: `[abc]`
* Ranges by scalar value: `[a-z]`
* Combination: `[a-zA-Z0-9]`

Character classes match exactly one scalar value from the specified set.

#### 5.7.1 Negated character classes

* `[^...]` matches one scalar value not in the specified set.

#### 5.7.2 Escapes inside character classes

Inside a character class, metacharacters are treated as literals except:

* `\` begins an escape
* `]` ends the class
* `-` denotes a range unless first or last
* `^` denotes negation only if first

Escapes allowed in classes are the same as outside classes.

### 5.8 Quantifiers

Quantifiers apply to the immediately preceding atom (literal, group, class, or dot).

Permitted quantifiers:

* `*` zero or more
* `+` one or more
* `?` zero or one
* `{n}` exactly n
* `{n,}` at least n
* `{n,m}` between n and m inclusive

Constraints:

* `n` and `m` are non-negative base-10 integers.
* If both are present, `n ≤ m`.
* Upper bounds MAY be limited by implementation policy, but must be at least 1,000.

Quantifiers are **greedy**.

Lazy (non-greedy) quantifiers are forbidden.

---

## 6. Escape Sequences (Permitted)

### 6.1 Literal escapes

The following escape sequences represent literal characters:

* `\\` backslash
* `\.` dot
* `\^` caret
* `\$` dollar
* `\|` vertical bar
* `\(` open parenthesis
* `\)` close parenthesis
* `\[` open bracket
* `\]` close bracket
* `\{` open brace
* `\}` close brace
* `\*` asterisk
* `\+` plus
* `\?` question mark
* `\-` hyphen

### 6.2 Control escapes

* `\n` LINE FEED (U+000A)
* `\r` CARRIAGE RETURN (U+000D)
* `\t` TAB (U+0009)

### 6.3 Unicode scalar escapes

* `\u{H}` where `H` is 1 to 6 hexadecimal digits, representing a Unicode scalar value.

The code point MUST be within the Unicode scalar value range and MUST NOT be a surrogate.

---

## 7. Forbidden Constructs

The following are invalid and MUST be rejected:

* backreferences (e.g. `\1`, `\k<name>`)
* lookahead and lookbehind (all forms)
* non-capturing groups `(?:...)`
* named capture groups
* inline flags (e.g. `(?i)`)
* lazy quantifiers (e.g. `*?`, `+?`, `{n,m}?`)
* word-boundary assertions (e.g. `\b`, `\B`)
* predefined character classes (e.g. `\d`, `\s`, `\w`)
* any engine-specific escapes not listed in this specification

---

## 8. Determinism and Safety Requirements

### 8.1 Deterministic results

All backends MUST produce identical Boolean results for identical inputs.

### 8.2 Performance

Implementations SHOULD avoid catastrophic backtracking.

Backends MAY implement this profile using:

* a Thompson NFA
* a DFA
* a bounded-backtracking engine

If a backend uses backtracking, it MUST enforce a step limit sufficient to ensure termination under all permitted patterns.

---

## 9. Conformance Tests (Required Coverage)

A conforming implementation MUST include test cases that cover at least:

* literal matching
* escaping metacharacters
* alternation
* grouping and precedence
* character classes and ranges
* negated character classes
* all quantifier forms
* anchors `^` and `$`
* `.` exclusion of line terminators
* `\u{...}` escapes
* rejection of forbidden constructs

---

## 10. SHACL Compilation

`MatchesRegularExpression` MUST compile to:

* SHACL `sh:pattern` when the pattern is representable under the SHACL regex subset in use, and
* a SHACL-SPARQL constraint when not.

Forbidden constructs MUST be rejected prior to compilation.
