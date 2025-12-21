import { assertEquals } from "@std/assert"
import * as fc from "fast-check"

import makePageContext from "./index.ts"

Deno.test("makePageContext", async function makePageContextTests(t) {
	await t.step(
		"creates a PageContext with url, params, and mode",
		function createsPageContext() {
			const url = new URL("http://example.com/about")
			const params = { id: "123" }
			const mode = "string" as const

			const context = makePageContext(url)(params)(mode)

			assertEquals(context.url, url)
			assertEquals(context.params, params)
			assertEquals(context.mode, mode)
		},
	)

	await t.step(
		"is curried - returns function after first call",
		function isCurriedFirstLevel() {
			const url = new URL("http://example.com")
			const withUrl = makePageContext(url)

			assertEquals(typeof withUrl, "function")
		},
	)

	await t.step(
		"is curried - returns function after second call",
		function isCurriedSecondLevel() {
			const url = new URL("http://example.com")
			const params = {}
			const withParams = makePageContext(url)(params)

			assertEquals(typeof withParams, "function")
		},
	)

	await t.step(
		"partial application preserves url across multiple calls",
		function partialApplicationPreservesUrl() {
			const url = new URL("http://example.com/test")
			const withUrl = makePageContext(url)

			const context1 = withUrl({ a: "1" })("dom")
			const context2 = withUrl({ b: "2" })("string")

			assertEquals(context1.url, url)
			assertEquals(context2.url, url)
		},
	)

	await t.step(
		"partial application preserves params across multiple calls",
		function partialApplicationPreservesParams() {
			const url = new URL("http://example.com")
			const params = { key: "value" }
			const withParams = makePageContext(url)(params)

			const context1 = withParams("dom")
			const context2 = withParams("string")

			assertEquals(context1.params, params)
			assertEquals(context2.params, params)
			assertEquals(context1.mode, "dom")
			assertEquals(context2.mode, "string")
		},
	)

	await t.step(
		"creates context with dom mode",
		function createsDomMode() {
			const url = new URL("http://example.com")
			const context = makePageContext(url)({})("dom")

			assertEquals(context.mode, "dom")
		},
	)

	await t.step(
		"creates context with string mode",
		function createsStringMode() {
			const url = new URL("http://example.com")
			const context = makePageContext(url)({})("string")

			assertEquals(context.mode, "string")
		},
	)
})

Deno.test(
	"makePageContext - property: url is preserved",
	function urlPreserved() {
		fc.assert(
			fc.property(
				fc.webUrl(),
				function checkUrlPreserved(urlString: string) {
					const url = new URL(urlString)
					const context = makePageContext(url)({})("string")

					return context.url === url
				},
			),
		)
	},
)

Deno.test(
	"makePageContext - property: params are preserved",
	function paramsPreserved() {
		fc.assert(
			fc.property(
				fc.dictionary(fc.string(), fc.string()),
				function checkParamsPreserved(params: Record<string, string>) {
					const url = new URL("http://example.com")
					const context = makePageContext(url)(params)("dom")

					return context.params === params
				},
			),
		)
	},
)

Deno.test(
	"makePageContext - property: mode is preserved",
	function modePreserved() {
		fc.assert(
			fc.property(
				fc.constantFrom("dom" as const, "string" as const),
				function checkModePreserved(mode: "dom" | "string") {
					const url = new URL("http://example.com")
					const context = makePageContext(url)({})(mode)

					return context.mode === mode
				},
			),
		)
	},
)
