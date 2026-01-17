Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# HTML Runtime DOM Binding Conventions

This specification defines the minimal DOM conventions required for the Paperhat **HTML Runtime** to bind a Presentation Plan payload to a rendered HTML document.

This document is **Normative**.

---

## 1. Purpose

HTML Runtime executes Behavior Programs (pure data) and applies their results to the DOM.

To do so deterministically, rendered HTML MUST expose stable identifiers for:

- Presentation Plan nodes
- fields used as binding sources

---

## 2. Scope

This specification governs:

- required `data-*` attributes used for runtime binding
- required behavior for `Validate`, `ShowIf`, and `EnableIf`

This specification does **not** govern:

- visual styling, UI widgets, or layout
- authoring semantics
- renderer implementation details beyond required attributes

---

## 3. Required Data Attribute (Normative)

HTML Runtime DOM binding MUST be expressed using exactly one attribute:

- `data-paperhat`

The value of `data-paperhat` MUST be a space-separated list of tokens.

Each token MUST have the form `key=value`.

### 3.0 Token Value Encoding

Token values MUST NOT contain ASCII whitespace characters.

If a binding identifier contains whitespace or other characters that would prevent it from appearing directly as a token value, the renderer MUST encode the value using percent-encoding:

- The token value MUST be encoded using UTF-8 bytes and percent-encoding as in RFC 3986 (for example, a space becomes `%20`).
- The HTML Runtime MUST percent-decode token values before interpreting them as `nodeId` or `fieldId`.

If percent-decoding fails, the runtime MUST treat the binding as missing (and apply the failure semantics in section 5).

Recognized keys in v0.1:

- `node` — binds an element to a Planned Node id
- `field` — binds a form control to a Presentation Plan `fieldId`

Unknown keys MUST be ignored.

### 3.1 Plan Node Binding

Any DOM element that represents a Planned Node MUST include:

- `data-paperhat` containing a `node=<nodeId>` token where `<nodeId>` equals the Planned Node `id`

The renderer MAY choose which specific element carries the token, but it MUST be stable and unique per node.

### 3.2 Field Binding

Any form control whose current value can be used as a binding source MUST include:

- `data-paperhat` containing a `field=<fieldId>` token where `<fieldId>` equals the `fieldId` referenced by a `FieldValue` binding source

The field element MUST be discoverable via `document.querySelectorAll('[data-paperhat]')`.

If an element contains both `node=<...>` and `field=<...>` tokens, the element participates in both bindings.

---

## 4. Attachment Application Semantics (Normative)

### 4.1 `ShowIf`

Given a `ShowIf` attachment on node `N`, the runtime MUST:

1. Evaluate the attachment’s `program` using:
   - `Argument` from `argument`
   - variables from `environment`
2. Interpret the result using the HTML Runtime conditional invalid policy.
3. Apply visibility by setting/removing the standard `hidden` attribute on the element whose `data-paperhat` contains `node=N`.

### 4.2 `EnableIf`

Given an `EnableIf` attachment on node `N`, the runtime MUST:

1. Evaluate the attachment’s `program` as in `ShowIf`.
2. Interpret the result using the HTML Runtime conditional invalid policy.
3. Enable/disable interactive controls inside the node element by setting `disabled` on:
   - any element within the node subtree that has a `data-paperhat` attribute containing a `field=<...>` token, and
   - any element within the node subtree that is a standard form control (`input`, `select`, `textarea`, `button`).

### 4.3 `Validate`

Given a `Validate` attachment on node `N`, the runtime MUST:

1. Evaluate the attachment’s `program` with `Argument` and `environment`.
2. If the result is `Invalid(diagnostics)`, the runtime MUST surface diagnostics by:
   - setting `aria-invalid="true"` on any element in the node subtree with a `data-paperhat` attribute containing a `field=<...>` token, and
   - exposing the diagnostics collection via a deterministic mechanism.

Diagnostic rendering mechanism is implementation-defined, but MUST be deterministic and MUST NOT require network access.

---

## 5. Failure Semantics (Normative)

If required DOM elements cannot be found for a referenced `nodeId` or `fieldId`, the runtime MUST treat the corresponding binding/evaluation as `Invalid(...)`.

---

**End of HTML Runtime DOM Binding Conventions v0.1**
