# Canonical Rule Traceability Matrix

This matrix maps every normative clause in `canonical-composition-construction-rules/index.md` to its enforcing mechanism.

Legend:

- **SHACL**: enforced by shape constraints in the core bundle (`wd-all.shacl.ttl`).
- **PROC**: enforced by deterministic pipeline/runtime procedure (non-SHACL algorithmic rule).

## §2 Ownership and sealing invariants

| Clause ID | Normative clause | Enforcement |
| --- | --- | --- |
| C2.1-1 | Every Structural Node has exactly one `wd:ownedBy` owner | SHACL: `wd-core-closure.shacl.ttl` (`*OwnershipShape` nodes) |
| C2.2-1 | Any node with `wd:ownedBy` must be a Structural Node class | SHACL: `wd-core-closure-seal.shacl.ttl` (`wd:OwnedNodeClassWhitelistShape`) |
| C2.3-1 | No cross-composition references across structural linking properties | SHACL: `wd-core-closure-seal.shacl.ttl` (`wd:CompositionSealShape`, 21 same-owner SPARQL constraints including `foreground/background`) |

## §3 Required construction rules

| Clause ID | Normative clause | Enforcement |
| --- | --- | --- |
| C3.1-1 | `wd:Composition` has exactly one `wd:hasCanvas` | SHACL: `wd-core.shacl.ttl` (`wd:CompositionShape`) |
| C3.1-2 | `wd:Composition` has at least one `wd:hasElement` | SHACL: `wd-core.shacl.ttl` (`wd:CompositionShape`) |
| C3.1-3 | `wd:Composition` has exactly one `wd:intent` | SHACL: `wd-core.shacl.ttl` (`wd:CompositionShape`) |
| C3.1-4 | Canvas referenced by composition is owned by that composition | SHACL: `wd-core-closure-seal.shacl.ttl` (`hasCanvas` same-owner SPARQL) |
| C3.2-1 | `wd:ElementInstance` has exactly one `wd:instanceOf` | SHACL: `wd-core.shacl.ttl` (`wd:ElementInstanceShape`) |
| C3.2-2 | `wd:ElementInstance` has exactly one `wd:frame` | SHACL: `wd-core.shacl.ttl` (`wd:ElementInstanceShape`) |
| C3.2-3 | `wd:ElementInstance` has exactly one `wd:style` | SHACL: `wd-core.shacl.ttl` (`wd:ElementInstanceShape`) |
| C3.2-4 | `wd:ElementInstance` has exactly one `wd:semanticRole` | SHACL: `wd-core.shacl.ttl` (`wd:ElementInstanceShape`) |
| C3.2-5 | `wd:ElementInstance` has exactly one `wd:zIndex` | SHACL: `wd-core.shacl.ttl` (`wd:ElementInstanceShape`) |
| C3.2-6 | Element/frame/style nodes are composition-owned | SHACL: `wd-core-closure.shacl.ttl` + `wd-core-closure-seal.shacl.ttl` |
| C3.2-7 | Optional transform node is composition-owned if present | SHACL: `wd-core-closure-seal.shacl.ttl` (`element.transform` same-owner) + `wd-core-closure.shacl.ttl` (`wd:TransformOwnershipShape`) |
| C3.3-1 | Rect has exactly one `wd:x` | SHACL: `wd-core.shacl.ttl` (`wd:RectShape`) |
| C3.3-2 | Rect has exactly one `wd:y` | SHACL: `wd-core.shacl.ttl` (`wd:RectShape`) |
| C3.3-3 | Rect has exactly one positive `wd:w` | SHACL: `wd-core.shacl.ttl` (`wd:RectShape`) |
| C3.3-4 | Rect has exactly one positive `wd:h` | SHACL: `wd-core.shacl.ttl` (`wd:RectShape`) |
| C3.4-1 | Style has exactly one opacity in `[0,1]` | SHACL: `wd-core.shacl.ttl` (`wd:StyleShape`) |
| C3.4-2 | `wd:fill` at most once | SHACL: `wd-core.shacl.ttl` (`wd:StyleShape`) |
| C3.4-3 | `wd:stroke` at most once | SHACL: `wd-core.shacl.ttl` (`wd:StyleShape`) |
| C3.4-4 | Fill paint is owned and has exactly one kind/value | SHACL: `wd-core-closure.shacl.ttl` + `wd-core.shacl.ttl` (`wd:PaintShape`) |
| C3.4-5 | Stroke is owned and has exactly one nonnegative width | SHACL: `wd-core-closure.shacl.ttl` + `wd-core.shacl.ttl` (`wd:StrokeShape`) |
| C3.4-6 | Type style is owned and satisfies typography minimum | SHACL: `wd-core-closure.shacl.ttl` + `wd-core.shacl.ttl` (`wd:TypographicStyleShape`) |
| C3.5-1 | Typographic style has exactly one typeface | SHACL: `wd-core.shacl.ttl` (`wd:TypographicStyleShape`) |
| C3.5-2 | Typographic style has exactly one positive fontSize | SHACL: `wd-core.shacl.ttl` (`wd:TypographicStyleShape`) |
| C3.5-3 | Typographic style has exactly one integer fontWeight >= 1 | SHACL: `wd-core.shacl.ttl` (`wd:TypographicStyleShape`) |
| C3.5-4 | Typographic style has exactly one positive leading | SHACL: `wd-core.shacl.ttl` (`wd:TypographicStyleShape`) |
| C3.5-5 | Tracking is optional, at most once | SHACL: `wd-core.shacl.ttl` (`wd:TypographicStyleShape`) |
| C3.6-1 | If grid exists, it is owned and has exactly one `columnCount >= 1` and `rowCount >= 1` | SHACL: `wd-core-grid.shacl.ttl` + `wd-core-closure-seal.shacl.ttl` |
| C3.6-2 | Grid units, if present, are owned | SHACL: `wd-core-closure.shacl.ttl` + `wd-core-closure-seal.shacl.ttl` |
| C3.6-3 | Grid unit must be exactly one of Column/Row/Gutter unit | SHACL: `wd-core-grid.shacl.ttl` (`wd:GridUnitShape`) |
| C3.6-4 | Baseline grid at most once and owned if present | SHACL: `wd-core-grid.shacl.ttl` + `wd-core-closure-seal.shacl.ttl` |
| C3.6-5 | Baseline step exactly once and > 0 | SHACL: `wd-core-grid.shacl.ttl` (`wd:BaselineGridShape`) |
| C3.7-1 | Principle statement has exactly one principleType | SHACL: `wd-core.shacl.ttl` (`wd:PrincipleStatementShape`) |
| C3.7-2 | Principle statement has exactly one scope | SHACL: `wd-core.shacl.ttl` (`wd:PrincipleStatementShape`) |
| C3.7-3 | Principle statement has one or more participants | SHACL: `wd-core.shacl.ttl` (`wd:PrincipleStatementShape`) |
| C3.7-4 | Principle statement is owned by composition | SHACL: `wd-core-closure.shacl.ttl` (`wd:PrincipleStatementOwnershipShape`) |
| C3.7-5 | Participants are element instances owned by composition | SHACL: `wd-core.shacl.ttl` + `wd-core-closure-seal.shacl.ttl` (`participant` same-owner) |
| C3.7-6 | Every owned principle statement is linked by `wd:expresses` | SHACL: `wd-core-closure-seal.shacl.ttl` (orphaned principle statement SPARQL) |
| C3.8-1 | Figure-ground statement has principle type `wd:FigureGround` | SHACL: `wd-core-figureground.shacl.ttl` (`wd:FigureGroundShape`) |
| C3.8-2 | Figure-ground statement has one or more foreground elements | SHACL: `wd-core-figureground.shacl.ttl` |
| C3.8-3 | Figure-ground statement has one or more background values | SHACL: `wd-core-figureground.shacl.ttl` |
| C3.8-4 | Every foreground is also a participant | SHACL: `wd-core-figureground.shacl.ttl` (`foreground-implies-participant` SPARQL) |
| C3.8-5 | Background is ElementInstance or Region, owned by composition | SHACL: `wd-core-figureground.shacl.ttl` + `wd-core-closure-seal.shacl.ttl` (`background` same-owner SPARQL) |

## §4 Canonical normalization rules

| Clause ID | Normative clause | Enforcement |
| --- | --- | --- |
| C4.1-1 | Ownership must be explicit, not inferred by reachability | SHACL: ownership shapes + reverse-reachability constraints in `wd-core-closure-seal.shacl.ttl` |
| C4.2-1 | No implicit cascade/group/z-order/snapping semantics | PROC: canonical graph materialization rules in pipeline; verified by deterministic canonical output checks |
| C4.3-1 | Defaults must be deterministic and materialized before hashing/validation | PROC: canonicalization pipeline contract |

## §5 Canonical serialization and hashing

| Clause ID | Normative clause | Enforcement |
| --- | --- | --- |
| C5.1-1 | NFC normalization precondition | PROC: canonical serialization step |
| C5.1-2 | No blank nodes in canonical graph | SHACL + PROC: whitelist + canonical serializer precheck |
| C5.2-1 | N-Triples canonical serialization and deterministic ordering | PROC: canonical serializer implementation contract |
| C5.3-1 | SHA-256 over canonical bytes, lowercase hex output | PROC: hasher implementation contract |
| C5.4-1 | Hash input scope is exactly canonical composition subgraph | PROC: graph extraction contract |

## §6 Validation contract

| Clause ID | Normative clause | Enforcement |
| --- | --- | --- |
| C6-1 | Valid iff §3, §2, §4, and full SHACL bundle pass | SHACL + PROC: validation orchestration contract |
| C6-2 | Any failed rule rejects composition | SHACL + PROC: validator fail-fast contract |
