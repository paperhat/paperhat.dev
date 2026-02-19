Status: WORKING
Lock State: LOCKED
Version: 1.0.0

# Design Policy Precedents 1.0.0

This note captures precedents that directly inform Workshop adaptive semantics.

## 1. Knuth-Plass precedent

Takeaway:

1. global optimization beats greedy local decisions
2. the cost function definition is the real specification

Workshop implication:

1. adaptive layout quality is defined as explicit badness terms
2. arrangement selection minimizes total badness under hard constraints
3. deterministic tie-break rules are mandatory

## 2. Muller-Brockmann precedent

Takeaway:

1. proportional relationships remain stable across format changes
2. grid systems are constraints, not fixed layouts

Workshop implication:

1. policies should declare relational/proportional structure, not pixel placements
2. reflow should preserve relationships when target dimensions change
3. responsiveness should be derived from feasibility thresholds, not manually authored breakpoint trees

## 3. Required optimization capabilities

A conforming adaptive optimization implementation MUST support:

1. hard constraints (must-pass)
2. soft weighted terms (tradeoff surface)
3. context-scoped activation of terms
4. satisfice mode and deterministic relaxation when infeasible
5. deterministic explanation output describing why an arrangement was selected

## 4. Contradiction handling

Principles can conflict (for example proximity vs contrast). Workshop resolves this by:

1. first enforcing hard constraints
2. then applying weighted optimization
3. then applying deterministic relaxation policy if needed
4. then deterministic lexical tie-breaks for any remaining equality

## 5. Override philosophy

Overrides are allowed for professional control, but are encoded as explicit constraints and re-run through the same solver path.

This preserves:

1. human authority
2. deterministic behavior
3. full auditability
