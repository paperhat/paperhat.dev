import { assertEquals } from "@std/assert"

import isHelp from "@sitebender/toolsmith/monads/result/guards/isHelp/index.ts"
import isOk from "@sitebender/toolsmith/monads/result/guards/isOk/index.ts"

import collectIndexFiles from "./index.ts"
import { COLLECT_INDEX_FILES_CODE } from "./constants/index.ts"

Deno.test("collectIndexFiles", async function collectIndexFilesTests(t) {
	await t.step(
		"returns AsyncIo with run function",
		function returnsAsyncIo() {
			const asyncIo = collectIndexFiles("./src/routing")

			assertEquals(asyncIo._tag, "AsyncIo")
			assertEquals(typeof asyncIo.run, "function")
		},
	)

	await t.step(
		"collects index.ts files from directory",
		async function collectsIndexFiles() {
			const asyncIo = collectIndexFiles("./src/routing")
			const result = await asyncIo.run()

			assertEquals(isOk(result), true)
			if (isOk(result)) {
				assertEquals(Array.isArray(result.value), true)
				assertEquals(result.value.length > 0, true)
				assertEquals(
					result.value.every(function endsWithIndexTs(f: string) {
						return f.endsWith("index.ts")
					}),
					true,
				)
			}
		},
	)

	await t.step(
		"filters out hidden paths",
		async function filtersHiddenPaths() {
			const asyncIo = collectIndexFiles("./src/routing")
			const result = await asyncIo.run()

			assertEquals(isOk(result), true)
			if (isOk(result)) {
				const hasHidden = result.value.some(function hasUnderscoreSegment(
					f: string,
				) {
					return f.split("/").some(function startsWithUnderscore(seg: string) {
						return seg.startsWith("_")
					})
				})

				assertEquals(hasHidden, false)
			}
		},
	)

	await t.step(
		"returns Help when root is not a string",
		async function returnsHelpForNonStringRoot() {
			const asyncIo = collectIndexFiles(123)
			const result = await asyncIo.run()

			assertEquals(isHelp(result), true)
			if (isHelp(result)) {
				assertEquals(result.help.code, COLLECT_INDEX_FILES_CODE.rootNotString)
			}
		},
	)

	await t.step(
		"returns Help when directory does not exist",
		async function returnsHelpForNonExistentDir() {
			const asyncIo = collectIndexFiles("./nonexistent-directory-12345")
			const result = await asyncIo.run()

			assertEquals(isHelp(result), true)
			if (isHelp(result)) {
				assertEquals(result.help.code, COLLECT_INDEX_FILES_CODE.walkFailed)
			}
		},
	)

	await t.step(
		"returns empty array for directory with no index.ts files",
		async function returnsEmptyForNoIndexFiles() {
			const asyncIo = collectIndexFiles("./coverage")
			const result = await asyncIo.run()

			assertEquals(isOk(result), true)
			if (isOk(result)) {
				assertEquals(result.value.length, 0)
			}
		},
	)
})
