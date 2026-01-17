Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary — Formatting

This specification defines the v0.1 **Formatting** family for the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

Formatting is intentionally separated from Behavior evaluation.

- Behavior is a deterministic expression language for computing values and boolean constraints.
- Presentation formatting, layout, localization, and target-specific rendering are projection concerns owned by the rendering and messaging specifications.

---

## 2. v0.1 Inventory (Normative)

In v0.1, the Behavior Vocabulary defines **no runtime formatting operators**.

Normative rule:

- Any operator whose purpose is locale-aware formatting (numbers, currencies, date/time, relative time, pluralization, etc.) MUST NOT be introduced as a v0.1 Behavior operator.

---

## 3. Relationship to Other Specifications

- Formatting intents for localized messaging are defined by Localized Messages and Locale Resolution.
- Diagnostic presentation rules are defined by Diagnostic Messaging and Help.

---

**End of Behavior Vocabulary — Formatting v0.1**
