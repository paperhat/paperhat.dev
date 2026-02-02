# Color Ramps (Workshop): E3 — Range + Semantics

This note sketches a **Workshop-level** convention for expressing color ramps without extending the Codex core value kinds.

The design uses **E3**: represent the endpoints as a `Range<Color>`, and attach **ramp semantics** as a separate record (space, step semantics, rules).

Codex core already treats `Range<T>` as a declarative interval whose semantics are **schema- or system-defined**; this document defines one such semantics package for Workshop usage.

---

## 1. Goals

- Keep ramp semantics **out of the Codex spec** (Workshop/schema-defined only).
- Avoid overloading a *color literal* to mean a *delta*.
- Make interpolation **explicit** (space + step meaning + edge rules).
- Preserve Codex’s posture that tools MUST NOT enumerate ranges; any “sampling” is an explicit Workshop operation.

---

## 2. Data Model (E3)

A color ramp value is represented as a **Record** with (at minimum) two fields:

- `range`: a `Range<Color>` (endpoints)
- `semantics`: a `Record` that describes how to interpret the range as a ramp

Conceptually:

```cdx
record[
	range: (<Color>..<Color>),
	semantics: record[
		space: <token>,
		endpointMode: <token>,
		step: <StepSpec>
	]
]
```

### 2.1 `space`

`space` selects the interpolation space/procedure. Recommended token set (extensible):

- `$srgb`
- `$oklab`
- `$oklch`
- `$hsl`
- `$lab`
- `$lch`

### 2.2 `endpointMode`

Defines whether endpoints must be expressed in the same surface form as the chosen space.

- `$strictSpelling` — endpoints MUST be spelled using the corresponding function form (e.g., `hsl(...)` for `$hsl`). No implicit conversions.
- `$convertToSpace` — endpoints may use any valid Codex color spelling; the Workshop system converts to the chosen space before interpolation.

Recommendation: default to `$strictSpelling` for determinism.

### 2.3 `step` (StepSpec)

`step` is a schema-defined record. Two recommended shapes:

- **By count**: `record[count: <PositiveInteger>]` meaning “this ramp intends to be sampled into N stops”.
- **By parameter delta**: `record[deltaT: <AnyRealNumber>]` where $t\in[0,1]$ and `deltaT` is the increment.

Optional add-ons:

- `includeEndpoints: Boolean` (default `true`)
- `clamp: Boolean` (default `true`)
- `huePath: $shorter | $longer | $increasing | $decreasing` (only meaningful for circular hue spaces)

Importantly: `step` is **not** a `Color`.

---

## 3. Suggested Validation Rules (Workshop)

These are rules a Workshop schema/validator should enforce.

1. `range` MUST be a `Range<Color>`.
2. `semantics` MUST be a Record.
3. `semantics.space` MUST be one of the supported space tokens.
4. `semantics.endpointMode` MUST be `$strictSpelling` or `$convertToSpace`.
5. `semantics.step` MUST match one of the supported step record shapes.

### 3.1 Strict spelling rules (recommended)

If `endpointMode=$strictSpelling`:

- `space=$hsl` → both endpoints MUST be spelled as `hsl(...)` (or `hsla(...)` if you decide to permit alpha explicitly for the ramp).
- `space=$oklab` → both endpoints MUST be spelled as `oklab(...)`.
- `space=$srgb` → endpoints MAY be `rgb(...)`/`rgba(...)` OR hexadecimal OR named colors, depending on how strict you want to be.

This keeps ramps from silently implying color conversion.

---

## 4. Examples

### 4.1 Neutral ramp (explicit space)

```cdx
<Thing ramp=record[
	range: &black..&white,
	semantics: record[
		space: $oklab,
		endpointMode: $convertToSpace,
		step: record[count: 9]
	]
] />
```

### 4.2 HSL lightness ramp with fixed hue/saturation

This is the intent you described, without making the `step` a color:

```cdx
<Thing ramp=record[
	range: hsl(0, 80%, 10%)..hsl(0, 80%, 90%),
	semantics: record[
		space: $hsl,
		endpointMode: $strictSpelling,
		step: record[
			deltaChannel: record[dh: 0, ds: 0%, dl: 10%]
		]
	]
] />
```

Notes:

- This requires Workshop to define the `deltaChannel` meaning for `$hsl`.
- A simpler variant is `step: record[count: 9]` (and let the system compute equal steps).

### 4.3 The tricky case

Input:

```cdx
hsl(0, 20%, 10%)..hsl(0, 80%, 90%)
```

Under E3 this is fine as a range of colors, but **it is not a well-defined ramp** without explicitly stating semantics.

If you tried to express the step as a color (the rejected Option D idea):

```cdx
hsl(0, 20%, 10%)..hsl(0, 80%, 90%)s hsl(0, 0%, 10%)
```

E3 avoids this ambiguity. You must instead choose one of:

- **Equal-parameter sampling** (e.g., `count: 9`), or
- **Channel deltas** (e.g., `dh/ds/dl`), including explicit rules about whether channels are treated as deltas, how hue wraps, and whether saturation/lightness are clamped.

---

## 5. Schema Sketch (Codex schema document)

This is intentionally a sketch: it uses a schema-defined named type plus a validator hook to enforce required fields.

```cdx
<Schema
	id=urn:paperhat:workshop:color-ramp
	version="0.1.0"
	versionScheme=$Semver
	compatibilityClass=$Initial
	authoringMode=$SimplifiedMode
	title="Workshop: Color Ramps"
	description="Schema-defined convention for color ramps expressed as range + semantics record."
>
	<EnumeratedValueSets>
		<EnumeratedValueSet id=urn:paperhat:workshop:enum:ColorRampSpace key=~colorRampSpace name="ColorRampSpace">
			<Member value="srgb" />
			<Member value="oklab" />
			<Member value="oklch" />
			<Member value="hsl" />
			<Member value="lab" />
			<Member value="lch" />
		</EnumeratedValueSet>
		<EnumeratedValueSet id=urn:paperhat:workshop:enum:ColorRampEndpointMode key=~colorRampEndpointMode name="ColorRampEndpointMode">
			<Member value="strictSpelling" />
			<Member value="convertToSpace" />
		</EnumeratedValueSet>
	</EnumeratedValueSets>

	<ValueTypeDefinitions>
		<ValueTypeDefinition
			id=urn:paperhat:workshop:vt:ColorRamp
			name="ColorRamp"
			baseValueType=$Record
			description="Record with fields: range: Range<Color>, semantics: Record. Semantics validated by a Workshop validator."
		/>
	</ValueTypeDefinitions>

	<TraitDefinitions>
		<TraitDefinition id=urn:paperhat:workshop:trait:ramp key=~ramp name="ramp" defaultValueType=$ColorRamp />
	</TraitDefinitions>

	<ConceptDefinitions>
		<ConceptDefinition id=urn:paperhat:workshop:concept:Thing name="Thing" />
	</ConceptDefinitions>

	<ValidatorDefinitions>
		<ValidatorDefinition
			id=urn:paperhat:workshop:validator:ColorRamp
			name="ColorRamp"
			description="Validates required fields and allowed combinations inside the ColorRamp record."
		/>
	</ValidatorDefinitions>
</Schema>
```

Implementation note:

- In Workshop you’d implement `ColorRamp` validation in your validator layer (e.g., SHACL-SPARQL or a deterministic host validator).
- This keeps the entire feature out of Codex core while still being schema-checkable in a Workshop pipeline.
