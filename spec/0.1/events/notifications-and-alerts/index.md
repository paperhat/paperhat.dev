Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Notifications and Alerts Specification

This specification defines Paperhat’s target-independent semantics for **notifications** and **alerts**.

This document governs semantic meaning and planning interfaces.
It does **not** define delivery channels (email, SMS, chat), vendor systems, message formats, or protocols.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* express notification intent as declarative workflow artifacts
* support auditable “who should know what, and why” semantics
* keep delivery and formatting as target realization concerns
* integrate notification intent with reliability, approvals, and run logs

---

## 2. Scope

This specification governs:

* notification and alert intent
* recipients as semantic identities and/or eligibility rules
* severity and classification
* deduplication intent (semantic)
* escalation intent (semantic)
* recordability requirements

This specification does **not** govern:

* delivery channels
* vendor message APIs
* templates or rendering
* localization

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)
* [Approvals and Human-in-the-Loop](../approvals-and-human-in-the-loop/)
* [Authentication and Authorization](../authentication-and-authorization/)

---

## 4. Core Invariants (Normative)

1. **Notification intent is data.** Notifications MUST be representable as declarative artifacts.
2. **No channel leakage.** Authored artifacts MUST NOT specify delivery channels or protocols.
3. **Auditability.** It MUST be possible to explain why a notification was emitted.
4. **Deterministic planning.** The Kernel MUST be able to plan notification emission deterministically.
5. **No secrets.** Notification intent MUST NOT require embedding secret material.

---

## 5. Definitions (Normative)

### 5.1 Notification

A **Notification** is a declarative intent to inform recipients about a subject.

A Notification MUST declare:

* notification identity
* subject reference (what it is about)
* classification and severity
* recipients (semantic)
* required provenance references

---

### 5.2 Alert

An **Alert** is a notification with stronger semantics, intended for urgent attention.

Alerts MUST support severity.

---

### 5.3 Recipient

A **Recipient** is a semantic description of who should receive a notification.

Recipients MAY be expressed as:

* explicit identity references
* eligibility rules (for example, role/capability based)

Recipients MUST be target-independent.

---

### 5.4 Notification Subject

A **NotificationSubject** is the semantic object of interest.

Subjects MAY refer to:

* a run
* a step attempt
* a policy application (retry exhausted, dead-letter created)
* an approval request

---

### 5.5 Severity

Severity is a semantic classification used for prioritization.

---

### 5.6 Deduplication Intent

A **DeduplicationIntent** is a declarative instruction intended to prevent repeated notifications for the same semantic condition.

Deduplication intent MUST NOT define a storage mechanism.

---

### 5.7 Escalation Intent

An **EscalationIntent** is a declarative instruction for follow-up notification behavior.

Escalation intent MUST NOT define delivery channels.

Time dependence MUST be explicit if escalation uses time.

---

## 6. Emission Semantics (Normative)

Notifications MAY be emitted from:

* explicit workflow steps
* policy-driven system behavior (for example, when dead-letter occurs)

Emission MUST be auditable and attributable to declared policy or declared workflow intent.

---

## 7. Authorization and Eligibility (Normative)

Notification emission MAY be subject to authorization policy.

Eligibility rules for recipients MUST be expressed in terms of semantic authorization constructs.

---

## 8. Reliability Interaction (Normative)

Reliability policy MAY influence whether a notification is emitted, but notification emission MUST remain auditable.

Notification emission MUST NOT be used as a retry mechanism.

---

## 9. Recordability (Normative)

Run logs MUST be able to record:

* notification identity
* subject reference
* severity/classification
* recipient rule references
* deduplication/escalation intent references (if present)
* why the notification was emitted

Records MUST NOT require embedding secrets.

---

## 10. Target Independence (Normative)

This specification MUST NOT define:

* email/SMS/chat protocols
* vendor systems
* templating

Targets may realize notifications with any appropriate mechanism, provided semantic meaning and recordability requirements are preserved.
