import { assertEquals } from "@std/assert"

import _wrapLayout from "./index.ts"
import type {
	LayoutFunction,
	PageContext,
	PageFunction,
} from "../../types/index.ts"
import type { VirtualNode } from "@sitebender/architect/types/index.ts"

//++ Helper to create a mock page function
function mockPage(id: string): PageFunction {
	return function mockPageFunction(_context: PageContext): VirtualNode {
		return { _tag: "text" as const, content: id }
	}
}

//++ Helper to create a mock layout function
function mockLayout(name: string): LayoutFunction {
	return function mockLayoutFunction(page: PageFunction): PageFunction {
		return function wrappedPage(context: PageContext): VirtualNode {
			const inner = page(context)
			return {
				_tag: "element" as const,
				tagName: name,
				attributes: {},
				children: [inner],
			}
		}
	}
}

Deno.test("_wrapLayout", async function wrapLayoutTests(t) {
	await t.step(
		"wraps page with layout",
		function wrapsPageWithLayout() {
			const page = mockPage("content")
			const layout = mockLayout("div")
			const wrapped = _wrapLayout(page, layout)

			assertEquals(typeof wrapped, "function")
		},
	)

	await t.step(
		"returns a PageFn that produces wrapped content",
		function producesWrappedContent() {
			const page = mockPage("content")
			const layout = mockLayout("section")
			const wrapped = _wrapLayout(page, layout)

			const context: PageContext = {
				url: new URL("http://example.com"),
				params: {},
				mode: "string",
			}
			const result = wrapped(context)

			assertEquals(result._tag, "element")
			if (result._tag === "element") {
				assertEquals(result.tagName, "section")
				assertEquals(result.children.length, 1)
				assertEquals(result.children[0], { _tag: "text", content: "content" })
			}
		},
	)

	await t.step(
		"applies layout to accumulator page",
		function appliesLayoutToAccumulator() {
			const page1 = mockPage("inner")
			const layout1 = mockLayout("article")
			const wrapped1 = _wrapLayout(page1, layout1)

			const layout2 = mockLayout("main")
			const wrapped2 = _wrapLayout(wrapped1, layout2)

			const context: PageContext = {
				url: new URL("http://example.com"),
				params: {},
				mode: "dom",
			}
			const result = wrapped2(context)

			assertEquals(result._tag, "element")
			if (result._tag === "element") {
				assertEquals(result.tagName, "main")
				assertEquals(result.children.length, 1)
				const firstChild = result.children[0]
				if (firstChild !== undefined && firstChild._tag === "element") {
					assertEquals(firstChild.tagName, "article")
				}
			}
		},
	)
})
