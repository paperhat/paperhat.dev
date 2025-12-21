import { assertEquals } from "@std/assert"
import * as fc from "fast-check"

import type { VirtualNode } from "@sitebender/architect/types/index.ts"

import compose from "./index.ts"
import type {
	LayoutFunction,
	PageContext,
	PageFunction,
} from "../types/index.ts"

//++ Helper to create a test context
function testContext(): PageContext {
	return {
		url: new URL("http://localhost/"),
		params: {},
		mode: "string",
	}
}

//++ Helper to create a simple text page
function textPage(content: string): PageFunction {
	return function page(_context: PageContext): VirtualNode {
		return { _tag: "text", content }
	}
}

//++ Helper to create a layout that wraps content in an element
function wrapInElement(tagName: string): LayoutFunction {
	return function layout(child: PageFunction): PageFunction {
		return function wrappedPage(context: PageContext): VirtualNode {
			return {
				_tag: "element",
				tagName,
				attributes: {},
				children: [child(context)],
			}
		}
	}
}

Deno.test("compose", async function composeTests(t) {
	await t.step(
		"returns function after first call (curried)",
		function returnsFunctionAfterFirstCall() {
			const layouts: ReadonlyArray<LayoutFunction> = []
			const composedLayouts = compose(layouts)

			assertEquals(typeof composedLayouts, "function")
		},
	)

	await t.step(
		"with empty layouts returns page unchanged",
		function emptyLayoutsReturnsPageUnchanged() {
			const layouts: ReadonlyArray<LayoutFunction> = []
			const page = textPage("Hello")

			const result = compose(layouts)(page)

			assertEquals(result, page)
		},
	)

	await t.step(
		"with one layout wraps page",
		function oneLayoutWrapsPage() {
			const layouts = [wrapInElement("div")]
			const page = textPage("Content")
			const context = testContext()

			const composed = compose(layouts)(page)
			const result = composed(context)

			assertEquals(result, {
				_tag: "element",
				tagName: "div",
				attributes: {},
				children: [{ _tag: "text", content: "Content" }],
			})
		},
	)

	await t.step(
		"with multiple layouts applies right-to-left",
		function multipleLayoutsRightToLeft() {
			const layouts = [
				wrapInElement("html"),
				wrapInElement("body"),
				wrapInElement("main"),
			]
			const page = textPage("Hello")
			const context = testContext()

			const composed = compose(layouts)(page)
			const result = composed(context)

			assertEquals(result, {
				_tag: "element",
				tagName: "html",
				attributes: {},
				children: [
					{
						_tag: "element",
						tagName: "body",
						attributes: {},
						children: [
							{
								_tag: "element",
								tagName: "main",
								attributes: {},
								children: [{ _tag: "text", content: "Hello" }],
							},
						],
					},
				],
			})
		},
	)

	await t.step(
		"partial application preserves layouts",
		function partialApplicationPreservesLayouts() {
			const layouts = [wrapInElement("section")]
			const withLayouts = compose(layouts)

			const page1 = textPage("Page 1")
			const page2 = textPage("Page 2")
			const context = testContext()

			const result1 = withLayouts(page1)(context)
			const result2 = withLayouts(page2)(context)

			assertEquals(result1, {
				_tag: "element",
				tagName: "section",
				attributes: {},
				children: [{ _tag: "text", content: "Page 1" }],
			})

			assertEquals(result2, {
				_tag: "element",
				tagName: "section",
				attributes: {},
				children: [{ _tag: "text", content: "Page 2" }],
			})
		},
	)

	await t.step(
		"passes context through all layouts to page",
		function passesContextThrough() {
			let capturedContext: PageContext | null = null

			function capturingPage(context: PageContext): VirtualNode {
				capturedContext = context
				return { _tag: "text", content: "captured" }
			}

			const layouts = [wrapInElement("div"), wrapInElement("span")]
			const context = testContext()

			compose(layouts)(capturingPage)(context)

			assertEquals(capturedContext, context)
		},
	)

	await t.step(
		"result is callable PageFunction",
		function resultIsCallablePageFunction() {
			const layouts: ReadonlyArray<LayoutFunction> = []
			const page = textPage("Test")
			const context = testContext()

			const composed = compose(layouts)(page)
			const result = composed(context)

			assertEquals(result, { _tag: "text", content: "Test" })
		},
	)
})

Deno.test(
	"compose - property: empty layouts returns identity",
	function emptyLayoutsIdentity() {
		fc.assert(
			fc.property(fc.string(), function checkIdentity(content: string) {
				const layouts: ReadonlyArray<LayoutFunction> = []
				const page = textPage(content)

				return compose(layouts)(page) === page
			}),
		)
	},
)

Deno.test(
	"compose - property: one layout wraps content",
	function oneLayoutWraps() {
		const tagArb = fc.stringMatching(/^[a-z]+$/).filter(function notEmpty(
			s: string,
		) {
			return s.length > 0
		})

		fc.assert(
			fc.property(
				tagArb,
				fc.string(),
				function checkWrapped(tagName: string, content: string) {
					const layouts = [wrapInElement(tagName)]
					const page = textPage(content)
					const context = testContext()

					const result = compose(layouts)(page)(context)

					return result._tag === "element" &&
						(result as {
								_tag: "element"
								tagName: string
								children: readonly VirtualNode[]
							}).tagName === tagName
				},
			),
		)
	},
)
