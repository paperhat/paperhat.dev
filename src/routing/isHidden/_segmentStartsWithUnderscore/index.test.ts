import { assertEquals } from "@std/assert"
import * as fc from "fast-check"

import _segmentStartsWithUnderscore from "./index.ts"

Deno.test(
	"_segmentStartsWithUnderscore",
	async function segmentStartsWithUnderscoreTests(t) {
		await t.step(
			"returns true when segment starts with underscore",
			function returnsTrueWhenStartsWithUnderscore() {
				assertEquals(_segmentStartsWithUnderscore("_private", 0, []), true)
				assertEquals(_segmentStartsWithUnderscore("_", 1, ["a"]), true)
				assertEquals(
					_segmentStartsWithUnderscore("_hidden", 2, ["a", "b", "c"]),
					true,
				)
			},
		)

		await t.step(
			"returns false when segment does not start with underscore",
			function returnsFalseWhenNoUnderscore() {
				assertEquals(_segmentStartsWithUnderscore("public", 0, []), false)
				assertEquals(_segmentStartsWithUnderscore("about", 1, ["a"]), false)
				assertEquals(_segmentStartsWithUnderscore("", 0, []), false)
			},
		)

		await t.step(
			"ignores index and array parameters",
			function ignoresIndexAndArray() {
				assertEquals(
					_segmentStartsWithUnderscore("_test", 0, []),
					_segmentStartsWithUnderscore("_test", 999, ["x", "y", "z"]),
				)
				assertEquals(
					_segmentStartsWithUnderscore("test", 0, []),
					_segmentStartsWithUnderscore("test", 42, ["a", "b"]),
				)
			},
		)
	},
)

Deno.test(
	"_segmentStartsWithUnderscore - property: result depends only on segment",
	function resultDependsOnlyOnSegment() {
		fc.assert(
			fc.property(
				fc.string(),
				fc.nat(),
				fc.array(fc.string()),
				function checkResultIndependentOfIndexAndArray(
					segment: string,
					index: number,
					array: ReadonlyArray<string>,
				) {
					const resultWithParams = _segmentStartsWithUnderscore(
						segment,
						index,
						array,
					)
					const resultWithDefaults = _segmentStartsWithUnderscore(
						segment,
						0,
						[],
					)

					return resultWithParams === resultWithDefaults
				},
			),
		)
	},
)

Deno.test(
	"_segmentStartsWithUnderscore - property: underscore prefix returns true",
	function underscorePrefixReturnsTrue() {
		fc.assert(
			fc.property(
				fc.string(),
				fc.nat(),
				fc.array(fc.string()),
				function checkUnderscorePrefix(
					suffix: string,
					index: number,
					array: ReadonlyArray<string>,
				) {
					return (
						_segmentStartsWithUnderscore("_" + suffix, index, array) === true
					)
				},
			),
		)
	},
)

Deno.test(
	"_segmentStartsWithUnderscore - property: non-underscore prefix returns false",
	function nonUnderscorePrefixReturnsFalse() {
		const nonUnderscoreStart = fc
			.string({ minLength: 1 })
			.filter(function notUnderscoreStart(s: string) {
				return !s.startsWith("_")
			})

		fc.assert(
			fc.property(
				nonUnderscoreStart,
				fc.nat(),
				fc.array(fc.string()),
				function checkNonUnderscorePrefix(
					segment: string,
					index: number,
					array: ReadonlyArray<string>,
				) {
					return _segmentStartsWithUnderscore(segment, index, array) === false
				},
			),
		)
	},
)
