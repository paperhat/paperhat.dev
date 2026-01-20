Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Behavior Vocabulary — Identity and Reference

This specification defines the **Identity and Reference operator family** for the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

This specification defines operations for identity and reference types:

- UUID operations
- IRI reference operations
- Lookup token operations

---

## 2. UUID Operations (Normative)

### 2.1 Construction

```
MakeUuid(string) -> Uuid
```

Error behavior:
- If invalid format: `Invalid(...)` with code `Identity::INVALID_UUID`.

### 2.2 Version Detection

```
UuidVersion(uuid) -> Integer
```

Returns: 1, 2, 3, 4, 5, 6, 7, or 8 depending on UUID version.

### 2.3 Variant Detection

```
UuidVariant(uuid) -> Text
```

Returns: "ncs", "rfc4122", "microsoft", or "future".

### 2.4 Component Extraction (v1, v6, v7)

```
UuidTimestamp(uuid) -> Instant
```

Error behavior:
- If not a time-based UUID: `Invalid(...)` with code `Identity::NOT_TIME_BASED_UUID`.

```
UuidClockSequence(uuid) -> Integer
UuidNode(uuid) -> Text
```

### 2.5 Formatting

```
UuidToString(uuid) -> Text
UuidToUpperCase(uuid) -> Text
UuidToLowerCase(uuid) -> Text
UuidToBytesHex(uuid) -> Text
```

`UuidToString` returns canonical lowercase with hyphens.
`UuidToBytesHex` returns 32 hex characters without hyphens.

### 2.6 Comparison

```
UuidsAreEqual(uuid1, uuid2) -> Boolean
```

Case-insensitive comparison.

### 2.7 Nil UUID

```
NilUuid() -> Uuid
```

Returns: 00000000-0000-0000-0000-000000000000

```
IsNilUuid(uuid) -> Boolean
```

### 2.8 Type Guard

```
IsUuid(value) -> Boolean
```

---

## 3. IRI Reference Operations (Normative)

### 3.1 Construction

```
MakeIriReference(string) -> IriReference
```

Error behavior:
- If invalid IRI: `Invalid(...)` with code `Identity::INVALID_IRI`.

### 3.2 Component Extraction

```
IriScheme(iri) -> Text
IriAuthority(iri) -> Text
IriPath(iri) -> Text
IriQuery(iri) -> Text
IriFragment(iri) -> Text
```

Returns `<Absent/>` if component is not present.

```
IriHost(iri) -> Text
IriPort(iri) -> Integer
IriUserInfo(iri) -> Text
```

### 3.3 Resolution

```
ResolveIri(base, reference) -> IriReference
```

Semantics:
- Resolves a relative reference against a base IRI per RFC 3986.

### 3.4 Normalization

```
NormalizeIri(iri) -> IriReference
```

Semantics:
- Applies syntax-based normalization (case, percent-encoding, path).

### 3.5 Formatting

```
IriToString(iri) -> Text
IriToUri(iri) -> Text
```

`IriToUri` encodes non-ASCII characters as percent-encoded UTF-8.

### 3.6 Comparison

```
IrisAreEquivalent(iri1, iri2) -> Boolean
```

Comparison after normalization.

### 3.7 Predicates

```
IsAbsoluteIri(iri) -> Boolean
IsRelativeIri(iri) -> Boolean
IriHasScheme(iri, scheme) -> Boolean
```

### 3.8 Type Guard

```
IsIriReference(value) -> Boolean
```

---

## 4. Lookup Token Operations (Normative)

### 4.1 Construction

```
MakeLookupToken(string) -> LookupToken
```

Error behavior:
- If not valid camelCase: `Invalid(...)` with code `Identity::INVALID_LOOKUP_TOKEN`.

### 4.2 Extraction

```
LookupTokenValue(token) -> Text
```

Returns the token string without the `~` sigil.

### 4.3 Formatting

```
LookupTokenToString(token) -> Text
```

Returns with `~` sigil (e.g., "~myToken").

### 4.4 Comparison

```
LookupTokensAreEqual(token1, token2) -> Boolean
```

### 4.5 Type Guard

```
IsLookupToken(value) -> Boolean
```

---

## 5. Enumerated Token Operations (Normative)

### 5.1 Construction

```
MakeEnumeratedToken(string) -> EnumeratedToken
```

Error behavior:
- If not valid identifier: `Invalid(...)` with code `Identity::INVALID_ENUMERATED_TOKEN`.

### 5.2 Extraction

```
EnumeratedTokenValue(token) -> Text
```

Returns the token string without the `$` sigil.

### 5.3 Formatting

```
EnumeratedTokenToString(token) -> Text
```

Returns with `$` sigil (e.g., "$Featured").

### 5.4 Comparison

```
EnumeratedTokensAreEqual(token1, token2) -> Boolean
```

### 5.5 Type Guard

```
IsEnumeratedToken(value) -> Boolean
```

---

**End of Behavior Vocabulary — Identity and Reference v0.1**
