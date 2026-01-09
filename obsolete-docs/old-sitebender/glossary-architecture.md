# Glossary Architecture

Paperhat uses a centralized glossary for terminology management, abbreviation
enforcement, and internationalization.

## Data Flow

```
CDX (source of truth)
        ↓ createElement
       IR
        ↓ serialize
    Triples
        ↓ persist
   Oxigraph (Pathfinder)
        ↓ SPARQL queries
   ┌────┴────┐
Steward   Linguist
(enforce) (translate)
        ↓ optional sync
  OpenMetadata (enterprise UI)
```

## Library Responsibilities

### Pathfinder

Owns the glossary data in the triple store.

- Stores terms, definitions, relationships as RDF triples
- Maintains abbreviation whitelist
- Aligns with ISO/IEC 11179 Conceptual Domains
- Provides SPARQL queries for term lookup

Example query: "Is `fn` a whitelisted abbreviation?"

```sparql
ASK {
  ?term a :Abbreviation ;
        :shortForm "fn" ;
        :whitelisted true .
}
```

### Linguist

Handles glossary term translations.

A glossary term is a translation problem — same concept, multiple locales.

```turtle
:term_button a :GlossaryTerm ;
  :label "button"@en ;
  :label "botón"@es ;
  :label "bouton"@fr ;
  :definition "A clickable UI element that triggers an action"@en ;
  :definition "Un elemento de UI en el que se puede hacer clic..."@es .
```

Linguist queries Pathfinder for localized term labels and definitions.

### Steward

Consumes the glossary for code style enforcement.

- Queries Pathfinder for the abbreviation whitelist
- Flags non-whitelisted abbreviations in code
- Suggests full terms for abbreviations

Example: `reduceWithFn` triggers a warning — "fn is not a whitelisted
abbreviation; use 'Function'"

Whitelisted abbreviations (examples):

- `HTML` — HyperText Markup Language
- `CSS` — Cascading Style Sheets
- `URL` — Uniform Resource Locator
- `API` — Application Programming Interface
- `ID` — Identifier
- `DOM` — Document Object Model

## Authoring

Glossary terms are authored in CDX like everything else in Paperhat.

```tsx
<Glossary>
	<Term id="button">
		<Label locale="en">button</Label>
		<Label locale="es">botón</Label>
		<Definition locale="en">
			A clickable UI element that triggers an action
		</Definition>
		<Abbreviation short="btn" allowed={false} />
	</Term>

	<Term id="url">
		<Label locale="en">URL</Label>
		<Definition locale="en">Uniform Resource Locator</Definition>
		<Abbreviation
			short="URL"
			allowed={true}
			expand="Uniform Resource Locator"
		/>
	</Term>
</Glossary>
```

This compiles to triples and persists in Oxigraph via the standard pipeline.

## OpenMetadata Integration (Optional)

OpenMetadata is an open-source data catalog with glossary features. It provides:

- Web UI for non-developers to view/browse terms
- Governance workflows (term approval, ownership)
- Audit trails and versioning
- Enterprise integration capabilities

### When to Use OpenMetadata

**Use it when:**

- Non-technical stakeholders need glossary access without touching CDX
- Enterprise customers require governance dashboards
- Demonstrating to funders who expect polished admin UIs
- Integrating with external enterprise data catalogs

**Skip it when:**

- Everyone authors in CDX
- Git provides sufficient collaboration/versioning
- SPARQL meets all query needs

### Sync Direction

CDX is the source of truth. OpenMetadata syncs FROM Oxigraph, not the reverse.

```
CDX → Oxigraph → OpenMetadata (read-only view)
```

OpenMetadata provides a presentation layer for enterprise stakeholders while
actual authoring remains in CDX.

### Implementation

OpenMetadata integration is Phase 5 in the Pathfinder roadmap. See
`pathfinder/ISO_IEC_11179_ALIGNMENT.md` for details on mapping glossary terms to
ISO/IEC 11179 Conceptual Domains.

## Use Cases

### 1. Abbreviation Enforcement

Steward enforces the "no abbreviations" rule by querying the whitelist.

```typescript
// Steward queries Pathfinder
const isAllowed = await query(`
  ASK { ?t a :Abbreviation ; :short "${abbrev}" ; :allowed true }
`);

if (!isAllowed) {
	warn(`"${abbrev}" is not a whitelisted abbreviation`);
}
```

### 2. Term Translations

Linguist renders glossary terms in the user's locale.

```tsx
<GlossaryTerm term="button" />
// Renders: "button" (en), "botón" (es), "bouton" (fr)
```

### 3. Documentation Generation

Query all terms for auto-generated glossary pages.

```sparql
SELECT ?term ?label ?definition WHERE {
  ?term a :GlossaryTerm ;
        :label ?label ;
        :definition ?definition .
  FILTER(lang(?label) = "en")
}
ORDER BY ?label
```

### 4. Enterprise Demos

Sync to OpenMetadata for stakeholder presentations without exposing CDX.
