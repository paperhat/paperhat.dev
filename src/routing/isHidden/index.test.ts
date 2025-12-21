import { assertEquals } from "@std/assert"
import * as fc from "fast-check"

import isHidden from "./index.ts"

Deno.test("isHidden", async function isHiddenTests(t) {
	await t.step(
		"returns true when path contains hidden segment",
		function returnsTrueWhenHiddenSegment() {
			assertEquals(isHidden("/_private"), true)
			assertEquals(isHidden("/a/_hidden/b"), true)
			assertEquals(isHidden("/_a/_b/_c"), true)
			assertEquals(isHidden("/public/_secret"), true)
		},
	)

	await t.step(
		"returns false when no segment starts with underscore",
		function returnsFalseWhenNoHiddenSegment() {
			assertEquals(isHidden("/public"), false)
			assertEquals(isHidden("/a/b/c"), false)
			assertEquals(isHidden("/about/contact"), false)
		},
	)

	await t.step(
		"returns false for empty string and root path",
		function returnsFalseForEmptyAndRoot() {
			assertEquals(isHidden(""), false)
			assertEquals(isHidden("/"), false)
		},
	)

	await t.step(
		"returns false for non-string inputs",
		function returnsFalseForNonString() {
			assertEquals(isHidden(123), false)
			assertEquals(isHidden(null), false)
			assertEquals(isHidden(undefined), false)
			assertEquals(isHidden({}), false)
			assertEquals(isHidden([]), false)
			assertEquals(isHidden(true), false)
		},
	)

	await t.step(
		"handles paths with underscores in middle of segment",
		function handlesMiddleUnderscores() {
			assertEquals(isHidden("/has_underscore"), false)
			assertEquals(isHidden("/a_b/c_d"), false)
			assertEquals(isHidden("/test_file/page"), false)
		},
	)

	await t.step(
		"handles deeply nested paths",
		function handlesDeeplyNestedPaths() {
			assertEquals(isHidden("/a/b/c/d/e/f/g"), false)
			assertEquals(isHidden("/a/b/c/_d/e/f/g"), true)
			assertEquals(isHidden("/a/b/c/d/e/f/_g"), true)
		},
	)
})

Deno.test(
	"isHidden - property: hidden segment means hidden path",
	function hiddenSegmentMeansHiddenPath() {
		const segmentArb = fc
			.stringMatching(/^[a-z0-9-]+$/)
			.filter(function hasContent(s: string) {
				return s.length > 0
			})

		fc.assert(
			fc.property(
				fc.array(segmentArb, { minLength: 0, maxLength: 5 }),
				segmentArb,
				fc.array(segmentArb, { minLength: 0, maxLength: 5 }),
				function checkHiddenSegment(
					before: ReadonlyArray<string>,
					hidden: string,
					after: ReadonlyArray<string>,
				) {
					const hiddenSegment = "_" + hidden
					const segments = [...before, hiddenSegment, ...after]
					const path = "/" + segments.join("/")

					return isHidden(path) === true
				},
			),
		)
	},
)

Deno.test(
	"isHidden - property: no underscore prefix means not hidden",
	function noUnderscorePrefixMeansNotHidden() {
		const segmentArb = fc
			.stringMatching(/^[a-z0-9][a-z0-9-]*$/)
			.filter(function hasContent(s: string) {
				return s.length > 0
			})

		fc.assert(
			fc.property(
				fc.array(segmentArb, { minLength: 1, maxLength: 5 }),
				function checkNoHiddenSegment(segments: ReadonlyArray<string>) {
					const path = "/" + segments.join("/")

					return isHidden(path) === false
				},
			),
		)
	},
)

Deno.test(
	"isHidden - property: non-string returns false",
	function nonStringReturnsFalse() {
		const nonStringArb = fc.oneof(
			fc.integer(),
			fc.double(),
			fc.boolean(),
			fc.constant(null),
			fc.constant(undefined),
			fc.object(),
			fc.array(fc.anything()),
		)

		fc.assert(
			fc.property(nonStringArb, function checkNonString(value: unknown) {
				return isHidden(value) === false
			}),
		)
	},
)
