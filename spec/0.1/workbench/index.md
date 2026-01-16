Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench v0.1 Index

---

## 1. Purpose

This document defines the authoritative specification set for **Paperhat Workbench v0.1** and how the documents relate.

---

## 2. Authoritative Workbench Specifications

### 2.1 Principles and Core Contracts

- [Workbench Principles](./workbench-principles/)
- [Workbench Contract](./workbench-contract/)
- [Core Contract](./core-contract/)
- [Core Command Protocol](./core-command-protocol/)

### 2.2 Workspace, Configuration, and Orchestration

- [Workspace Filesystem Contract](./filesystem-contract/)
- [Workspace Configuration Contract](./workspace-configuration-contract/)
- [Preview and Build Orchestration Contract](./preview-and-build-orchestration-contract/)

### 2.3 Templates and Authoring Support

- [Template Format](./template-format/)
- [Templates and File Plans](./templates-and-file-plans/)
- [ConceptForm Contract](./conceptform-contract/)
- [Authoring Projections Contract](./authoring-projections-contract/)
- [Assistive Authoring Contract](./assistive-authoring-contract/)

### 2.4 Diagnostics and Explanation

- [Diagnostic Messaging and Help](./diagnostic-messaging-and-help/)
- [Introspection and Explanation Contract](./introspection-and-explanation-contract/)

---

## 3. Cross-References (Non-exhaustive)

- Workspace operations assume the workspace layout defined by the [Workspace Filesystem Contract](./filesystem-contract/).
- Target definitions, target identifiers, and target selection requirements are governed by the [Workspace Configuration Contract](./workspace-configuration-contract/) and are consumed by the [Preview and Build Orchestration Contract](./preview-and-build-orchestration-contract/).
- Template parsing rules are defined by [Template Format](./template-format/); template application and planned file emission are defined by [Templates and File Plans](./templates-and-file-plans/).
- User-facing errors, refusals, and help guidance use [Diagnostic Messaging and Help](./diagnostic-messaging-and-help/).
- Explanation and structured “why” surfaces use the [Introspection and Explanation Contract](./introspection-and-explanation-contract/).

---

**End of Workbench Index v0.1**
