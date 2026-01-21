Status: DRAFT
Version: 0.1

# Schema Hierarchy Specification

This specification defines the three-level schema hierarchy that enables Workshop to bootstrap itself and validate all authored content.

This document is **Normative**.

---

## 1. Purpose

Workshop must parse and validate Codex documents. To do this, it needs to understand what constructs are valid in each document type. The schema hierarchy solves the bootstrapping problem: how does Workshop know how to parse schemas if schemas define what can be parsed?

The answer is a three-level hierarchy:

1. **Bootstrap Schema** — hardcoded into Workshop
2. **Meta Schemas** — define categories of schemas
3. **Domain Schemas** — define concrete ontologies

Each level authorizes the level below it.

---

## 2. The Three Levels

### 2.1 Bootstrap Schema (Schema-of-Schemas)

The Bootstrap Schema is **built into Workshop**. It is not authored in Codex; it is intrinsic to the implementation.

The Bootstrap Schema defines the primitive constructs that all other schemas use:

- `Schema` — the root concept for any schema document
- `ConceptDefinition` — declares a concept that may appear in documents
- `TraitDefinition` — declares a trait (attribute) that concepts may carry
- `ConstraintDefinition` — declares validation rules
- Structural constructs for rules: `ContentRules`, `ChildRules`, `TraitRules`, `CollectionRules`
- Constraint targeting: `Targets`, `TargetConcept`, `TargetContext`
- Constraint logic: `Rule`, `ForAll`, `Not`, etc.

Without the Bootstrap Schema, Workshop cannot parse anything. With it, Workshop can parse Meta Schemas.

Rules:

- The Bootstrap Schema is **not user-modifiable**.
- The Bootstrap Schema is **versioned with Workshop itself**.
- All Meta Schemas must conform to the Bootstrap Schema.

---

### 2.2 Meta Schemas

Meta Schemas define **categories of schemas**. They specify what a particular type of schema may contain and what it must forbid.

Examples of Meta Schemas:

| Meta Schema | Purpose |
|-------------|---------|
| `codex:meta:data` | Authorizes domain ontology schemas |
| `codex:meta:view` | Authorizes view definition schemas |
| `codex:meta:policy` | Authorizes design policy schemas |
| `codex:meta:intent` | Authorizes design intent schemas |

Each Meta Schema acts as a **gatekeeper** for its category. For example, the Data Meta-Schema (`codex:meta:data`) declares:

- Domain schemas may define `DomainConcept` (semantic concepts for the ontology)
- Domain schemas must NOT define individuals (`MustBeEntity` is forbidden at schema level)
- Content is forbidden by default in domain concepts (must be explicitly allowed)
- Collection ordering must be declared

Meta Schemas are authored in Codex and parsed using the Bootstrap Schema.

Location:

```
schemas/meta/{category}/schema.cdx
```

Rules:

- Meta Schemas conform to the Bootstrap Schema.
- Meta Schemas constrain what Domain Schemas may declare.
- Each artifact category (data, view, policy, etc.) has exactly one Meta Schema.

---

### 2.3 Domain Schemas

Domain Schemas define **concrete ontologies** for specific subject matter. They are authored by domain experts (or those who understand the domain) and describe the structure of data in that domain.

Examples of Domain Schemas:

| Domain Schema | Purpose |
|---------------|---------|
| `codex:domain:recipe` | Defines Recipe, Ingredient, Step, etc. |
| `codex:domain:product` | Defines Product, Price, Variant, etc. |
| `codex:domain:article` | Defines Article, Section, Author, etc. |

A Domain Schema defines:

- **Concepts** — the classes in the ontology (e.g., `Recipe`, `Ingredient`)
- **Traits** — the attributes concepts may carry (e.g., `name`, `amount`, `unit`)
- **Constraints** — validation rules (e.g., "Recipe requires Title")
- **Entity eligibility** — whether instances of a concept are individuals (`MustBeEntity`) or structural parts (`MustNotBeEntity`)

Location:

```
schemas/domains/{domain}/schema.cdx
```

Rules:

- Domain Schemas conform to their governing Meta Schema.
- Domain Schemas define the ontology; they do not define individuals.
- Data files (individuals) conform to Domain Schemas.

---

## 3. Authorization Flow

```
Bootstrap Schema (hardcoded in Workshop)
         │
         │ authorizes parsing of
         ▼
    Meta Schemas
         │
         │ authorize structure of
         ▼
   Domain Schemas
         │
         │ authorize structure of
         ▼
    Data Files (individuals)
```

Each level validates the level below:

- Workshop validates Meta Schemas against the Bootstrap Schema
- Workshop validates Domain Schemas against their Meta Schema
- Workshop validates Data Files against their Domain Schema

---

## 4. Semantic Mapping

The schema hierarchy maps to OWL2/SHACL semantic web primitives:

| Codex Construct | Semantic Web Equivalent |
|-----------------|------------------------|
| `ConceptDefinition` with `MustBeEntity` | OWL2 Class (for individuals) |
| `ConceptDefinition` with `MustNotBeEntity` | Structural component (blank node or nested structure) |
| `TraitDefinition` | OWL2 Property |
| `ConstraintDefinition` | SHACL Shape |
| Data file instance | OWL2 Individual (instance of a class) |

Domain Schemas are ontologies. Data files are individuals in those ontologies.

---

## 5. Example

### Meta Schema (excerpt from `codex:meta:data`)

```cdx
<Schema id=codex:meta:data ...>
  <ConceptDefinitions>
    <ConceptDefinition
      name="DomainConcept"
      conceptKind=$Semantic
      entityEligibility=$MayBeEntity
    >
      <ContentRules>
        <ForbidsContent />
      </ContentRules>
    </ConceptDefinition>
  </ConceptDefinitions>
  
  <ConstraintDefinitions>
    <ConstraintDefinition id=codex:meta:data:no-instances ...>
      <!-- Domain schemas must not define individuals -->
    </ConstraintDefinition>
  </ConstraintDefinitions>
</Schema>
```

### Domain Schema (excerpt from `codex:domain:recipe`)

```cdx
<Schema id=codex:domain:recipe ...>
  <ConceptDefinitions>
    <ConceptDefinition
      name="Recipe"
      conceptKind=$Semantic
      entityEligibility=$MustBeEntity
    >
      <ChildRules>
        <AllowsChildConcept conceptSelector="Title" />
        <AllowsChildConcept conceptSelector="Ingredients" />
        <AllowsChildConcept conceptSelector="Instructions" />
      </ChildRules>
    </ConceptDefinition>
    
    <ConceptDefinition
      name="Ingredient"
      conceptKind=$Semantic
      entityEligibility=$MustNotBeEntity
    >
      <TraitRules>
        <RequiresTrait name="name" />
        <AllowsTrait name="amount" />
      </TraitRules>
    </ConceptDefinition>
  </ConceptDefinitions>
</Schema>
```

### Data File (individual)

```cdx
<Recipe id=recipe:chocolate-chip-cookies>
  <Title>Chocolate Chip Cookies</Title>
  <Ingredients>
    <Ingredient name="flour" amount=2 unit="cups" />
    <Ingredient name="chocolate chips" amount=1 unit="cup" />
  </Ingredients>
  <Instructions>
    <Step>Preheat oven to 375°F.</Step>
    <Step>Mix dry ingredients.</Step>
  </Instructions>
</Recipe>
```

---

## 6. Summary

- The **Bootstrap Schema** is hardcoded and enables Workshop to parse anything
- **Meta Schemas** define categories of schemas and constrain what they may contain
- **Domain Schemas** define concrete ontologies for specific subject matter
- **Data Files** are individuals conforming to Domain Schemas
- Each level authorizes and validates the level below it

---

**End of Schema Hierarchy Specification v0.1**
