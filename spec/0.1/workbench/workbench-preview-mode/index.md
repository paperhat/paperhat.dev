Status: NORMATIVE  
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Workbench Preview Mode

This specification defines Workbench behavior for preview mode across multiple targets.

This document is **Normative**.

---

## 1. Purpose

Preview mode is for development, not production. It watches workspace files and updates output when they change.

Workbench preview mode exists to:

- watch for changes to authored content
- rebuild deterministically on workspace changes
- present a local preview surface

---

## 2. Target Selection (Normative)

Workbench MUST support selecting a target (for example: HTML web app, ebook, PDF).

Rules:

1. Target selection MUST be explicit.
2. Workbench MUST NOT silently change targets based on environment.

---

## 3. Watch Loop (Normative)

In preview mode, Workbench MUST:

- watch the workspace `modules/` for changes
- re-run the appropriate steps deterministically
- surface diagnostics on failure without corrupting the workspace

---

## 4. Preview Surface (Normative)

Workbench MUST provide a local preview surface for preview mode.

Implementation MAY include a server whose configuration/runtime is housed under `.paperhat/`.

Workbench MUST NOT require network access to external services to serve local previews.

---

**End of Workbench Preview Mode v0.1**
