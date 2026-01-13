## XHTML failed because it put the contract in the wrong place

XML was never about angle brackets.
It was about **contracts**:

* well-formedness
* explicit structure
* namespaces
* machine-verifiable meaning

XHTML tried to enforce that contract **at the browser boundary**, where:

* authors are anonymous
* tools are inconsistent
* error tolerance is mandatory
* commercial incentives reward permissiveness

That was always doomed.

The web had already crossed the point where runtime strictness was socially acceptable.

---

## The fatal XHTML mistake

XHTML assumed:

> “If the browser refuses to render incorrect documents, authors will learn to do better.”

The reality was:

> “If the browser refuses to render incorrect documents, authors will abandon it.”

WHATWG didn’t win because they were wrong.
They won because they optimized for **ecosystem survival**.

Correctness lost to scale.

---

## Paperhat fixes the mistake, not the syntax

Paperhat moves the contract **upstream**:

| Layer                | Responsibility                  |
| -------------------- | ------------------------------- |
| Authoring (Codex)    | Rigor, semantics, correctness   |
| Compiler (Paperhat)  | Validation, assembly, reasoning |
| Outputs (HTML, etc.) | Serialization only              |
| Browser              | Rendering and interaction       |

This is what XML *should* have been used for on the Web:
**intermediate representation**, not runtime substrate.

---

## Why real XML / namespaces are still the wrong output

Yes, browsers can parse XML.
Yes, namespaces technically work.
Yes, XSL-FO still limps along.

But:

* Copy/paste breaks
* Toolchains break
* CMSs break
* Sanitizers break
* Humans break it accidentally

And worst of all:

* **The browser becomes a correctness gate again**

That’s a regression, not a victory.

Paperhat deliberately refuses to give browsers that authority.

---

## The uncomfortable truth

> If browser vendors actually cared about semantic documents, Paperhat wouldn’t need to exist.

But they don’t — and never did.

They care about:

* market share
* engagement
* revenue
* survivability

User experience and document quality are *emergent properties*, not goals.

So Paperhat opts out.

---

## Why `data-paperhat` is philosophically correct

Using:

```html
data-paperhat="concept=Recipe"
```

is not compromise. It is **containment**.

It says:

* “This document has real semantics”
* “HTML is not trusted to carry them”
* “Meaning lives outside the DOM contract”

That is the XML worldview, implemented where it actually works.

---

## The future is Paperhat

Paperhat is the only way to:

* Use real XML
* Use real namespaces
* Use real semantics
* Use real correctness

…and still get the Web to work.
