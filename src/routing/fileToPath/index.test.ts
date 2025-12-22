import { assertEquals } from "@std/assert"
import * as fc from "fast-check"

import isHelp from "@sitebender/toolsmith/monads/result/guards/isHelp/index.ts"
import isOk from "@sitebender/toolsmith/monads/result/guards/isOk/index.ts"

import fileToPath from "./index.ts"
import { FILE_TO_PATH_CODE } from "./constants/index.ts"

Deno.test("fileToPath", async function fileToPathTests(t) {
	await t.step(
		"converts file path to route path",
		function convertsFilePath() {
			const result = fileToPath("/pages")("/pages/about/index.ts")

			assertEquals(isOk(result), true)
			if (isOk(result)) {
				assertEquals(result.value, "/about")
			}
		},
	)

	await t.step(
		"converts root index.ts to /",
		function convertsRootIndex() {
			const result = fileToPath("/pages")("/pages/index.ts")

			assertEquals(isOk(result), true)
			if (isOk(result)) {
				assertEquals(result.value, "/")
			}
		},
	)

	await t.step(
		"handles deeply nested paths",
		function handlesDeeplyNested() {
			const result = fileToPath("/pages")("/pages/a/b/c/index.ts")

			assertEquals(isOk(result), true)
			if (isOk(result)) {
				assertEquals(result.value, "/a/b/c")
			}
		},
	)

	await t.step(
		"is curried - returns function after first call",
		function isCurried() {
			const fromPages = fileToPath("/pages")

			assertEquals(typeof fromPages, "function")
		},
	)

	await t.step(
		"partial application preserves root",
		function partialApplicationWorks() {
			const fromPages = fileToPath("/pages")

			const about = fromPages("/pages/about/index.ts")
			const contact = fromPages("/pages/contact/index.ts")

			assertEquals(isOk(about), true)
			assertEquals(isOk(contact), true)
			if (isOk(about) && isOk(contact)) {
				assertEquals(about.value, "/about")
				assertEquals(contact.value, "/contact")
			}
		},
	)

	await t.step(
		"returns Help when root is not a string",
		function returnsHelpForNonStringRoot() {
			const result = fileToPath(123)("/pages/index.ts")

			assertEquals(isHelp(result), true)
			if (isHelp(result)) {
				assertEquals(result.help.code, FILE_TO_PATH_CODE.rootNotString)
			}
		},
	)

	await t.step(
		"returns Help when file is not a string",
		function returnsHelpForNonStringFile() {
			const result = fileToPath("/pages")(456)

			assertEquals(isHelp(result), true)
			if (isHelp(result)) {
				assertEquals(result.help.code, FILE_TO_PATH_CODE.fileNotString)
			}
		},
	)

	await t.step(
		"returns Help for non-string root before checking file",
		function checksRootFirst() {
			const result = fileToPath(null)(undefined)

			assertEquals(isHelp(result), true)
			if (isHelp(result)) {
				assertEquals(result.help.code, FILE_TO_PATH_CODE.rootNotString)
			}
		},
	)
})

Deno.test(
	"fileToPath - property: valid paths produce Ok",
	function validPathsProduceOk() {
		const segmentArb = fc
			.stringMatching(/^[a-z0-9-]+$/)
			.filter(function hasContent(s: string) {
				return s.length > 0
			})

		fc.assert(
			fc.property(
				segmentArb,
				fc.array(segmentArb, { minLength: 0, maxLength: 4 }),
				function checkValidPaths(
					rootName: string,
					segments: ReadonlyArray<string>,
				) {
					const root = "/" + rootName
					const filePath = root + "/" + segments.join("/") + "/index.ts"
					const result = fileToPath(root)(filePath)

					return isOk(result)
				},
			),
		)
	},
)

Deno.test(
	"fileToPath - property: non-string root returns Help",
	function nonStringRootReturnsHelp() {
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
			fc.property(
				nonStringArb,
				fc.string(),
				function checkNonStringRoot(root: unknown, file: string) {
					const result = fileToPath(root)(file)

					if (isHelp(result)) {
						return result.help.code === FILE_TO_PATH_CODE.rootNotString
					}
					return false
				},
			),
		)
	},
)

Deno.test(
	"fileToPath - property: non-string file returns Help",
	function nonStringFileReturnsHelp() {
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
			fc.property(
				fc.string(),
				nonStringArb,
				function checkNonStringFile(root: string, file: unknown) {
					const result = fileToPath(root)(file)

					if (isHelp(result)) {
						return result.help.code === FILE_TO_PATH_CODE.fileNotString
					}
					return false
				},
			),
		)
	},
)
