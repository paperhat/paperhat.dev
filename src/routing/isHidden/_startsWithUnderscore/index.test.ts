import { assertEquals } from "@std/assert"
import * as fc from "fast-check"

import _startsWithUnderscore from "./index.ts"

Deno.test("_startsWithUnderscore", async function startsWithUnderscoreTests(t) {
	await t.step(
		"returns true when segment starts with underscore",
		function returnsTrueWhenStartsWithUnderscore() {
			assertEquals(_startsWithUnderscore("_private"), true)
			assertEquals(_startsWithUnderscore("_"), true)
			assertEquals(_startsWithUnderscore("_hidden"), true)
			assertEquals(_startsWithUnderscore("__double"), true)
		},
	)

	await t.step(
		"returns false when segment does not start with underscore",
		function returnsFalseWhenNoUnderscore() {
			assertEquals(_startsWithUnderscore("public"), false)
			assertEquals(_startsWithUnderscore("about"), false)
			assertEquals(_startsWithUnderscore(""), false)
			assertEquals(_startsWithUnderscore("has_underscore"), false)
		},
	)

	await t.step(
		"only checks first character",
		function onlyChecksFirstCharacter() {
			assertEquals(_startsWithUnderscore("a_b"), false)
			assertEquals(_startsWithUnderscore("test_file"), false)
			assertEquals(_startsWithUnderscore("_test_file"), true)
		},
	)
})

Deno.test(
	"_startsWithUnderscore - property: underscore prefix returns true",
	function underscorePrefixReturnsTrue() {
		fc.assert(
			fc.property(
				fc.string(),
				function checkUnderscorePrefix(suffix: string) {
					return _startsWithUnderscore("_" + suffix) === true
				},
			),
		)
	},
)

Deno.test(
	"_startsWithUnderscore - property: non-underscore prefix returns false",
	function nonUnderscorePrefixReturnsFalse() {
		const nonUnderscoreStart = fc
			.string({ minLength: 1 })
			.filter(function notUnderscoreStart(s: string) {
				return !s.startsWith("_")
			})

		fc.assert(
			fc.property(
				nonUnderscoreStart,
				function checkNonUnderscorePrefix(segment: string) {
					return _startsWithUnderscore(segment) === false
				},
			),
		)
	},
)
