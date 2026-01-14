Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Workbench Dev Watch and Targets

This specification defines Workbench behavior for dev/watch mode across multiple targets.

This document is **Normative**.

---

## 1. Purpose

Workbench dev mode exists to:

- run in watch mode
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

In dev/watch mode, Workbench MUST:

- watch the workspace `modules/` for changes
- re-run the appropriate steps deterministically
- surface diagnostics on failure without corrupting the workspace

---

## 4. Preview Surface (Normative)

Workbench MUST provide a local preview surface for dev mode.

Implementation MAY include a dev server whose configuration/runtime is housed under `.paperhat/`.

Workbench MUST NOT require network access to external services to serve local previews.

---

**End of Workbench Dev Watch and Targets v0.1**
