import { assertEquals } from "@std/assert"
import * as fc from "fast-check"

import type { VirtualNode } from "@sitebender/architect/types/index.ts"

import renderRoute from "./index.ts"
import Route from "../Route/index.ts"
import type { PageContext, PageFunction } from "../types/index.ts"

//++ Helper to create a mock page that returns specific content
function mockPage(content: string) {
	return function page(_context: PageContext): VirtualNode {
		return { _tag: "text" as const, content }
	}
}

//++ Helper to create a mock route with a given path and content
function mockRoute(path: string, content: string) {
	return Route(path)(function mockLoad(): Promise<PageFunction> {
		return Promise.resolve(mockPage(content))
	})
}

//++ Helper to create a standard test context
function testContext(path: string): PageContext {
	return {
		url: new URL(`http://localhost${path}`),
		params: {},
		mode: "string",
	}
}

Deno.test("renderRoute", async function renderRouteTests(t) {
	await t.step(
		"returns async function after first call",
		function returnsAsyncFunction() {
			const route = mockRoute("/", "home")
			const render = renderRoute(route)

			assertEquals(typeof render, "function")
		},
	)

	await t.step(
		"renders page with context and returns VirtualNode",
		async function rendersPageWithContext() {
			const route = mockRoute("/about", "About Page")
			const render = renderRoute(route)
			const context = testContext("/about")

			const result = await render(context)

			assertEquals(result, { _tag: "text", content: "About Page" })
		},
	)

	await t.step(
		"passes context to page function",
		async function passesContextToPage() {
			let capturedContext: PageContext | null = null

			const route = Route("/test")(
				function loadCapture(): Promise<PageFunction> {
					return Promise.resolve(
						function capturePage(context: PageContext): VirtualNode {
							capturedContext = context
							return { _tag: "text", content: "captured" }
						},
					)
				},
			)

			const context = testContext("/test")
			await renderRoute(route)(context)

			assertEquals(capturedContext, context)
		},
	)

	await t.step(
		"is curried - can be partially applied",
		async function isCurried() {
			const homeRoute = mockRoute("/", "Home")
			const aboutRoute = mockRoute("/about", "About")

			const renderHome = renderRoute(homeRoute)
			const renderAbout = renderRoute(aboutRoute)

			const homeContext = testContext("/")
			const aboutContext = testContext("/about")

			const homeResult = await renderHome(homeContext)
			const aboutResult = await renderAbout(aboutContext)

			assertEquals(homeResult, { _tag: "text", content: "Home" })
			assertEquals(aboutResult, { _tag: "text", content: "About" })
		},
	)

	await t.step(
		"works with element VirtualNodes",
		async function worksWithElements() {
			const route = Route("/element")(
				function loadElement(): Promise<PageFunction> {
					return Promise.resolve(function elementPage(): VirtualNode {
						return {
							_tag: "element",
							tagName: "div",
							attributes: { class: "container" },
							children: [{ _tag: "text", content: "Hello" }],
						}
					})
				},
			)

			const result = await renderRoute(route)(testContext("/element"))

			assertEquals(result, {
				_tag: "element",
				tagName: "div",
				attributes: { class: "container" },
				children: [{ _tag: "text", content: "Hello" }],
			})
		},
	)

	await t.step(
		"works with context containing params",
		async function worksWithParams() {
			let capturedParams: Record<string, string> = {}

			const route = Route("/user/:id")(
				function loadUser(): Promise<PageFunction> {
					return Promise.resolve(
						function userPage(context: PageContext): VirtualNode {
							capturedParams = context.params as Record<string, string>
							return { _tag: "text", content: `User: ${context.params["id"]}` }
						},
					)
				},
			)

			const context: PageContext = {
				url: new URL("http://localhost/user/123"),
				params: { id: "123" },
				mode: "string",
			}

			await renderRoute(route)(context)

			assertEquals(capturedParams, { id: "123" })
		},
	)

	await t.step(
		"works with dom mode context",
		async function worksWithDomMode() {
			let capturedMode: "dom" | "string" = "string"

			const route = Route("/dom")(function loadDom(): Promise<PageFunction> {
				return Promise.resolve(
					function domPage(context: PageContext): VirtualNode {
						capturedMode = context.mode
						return { _tag: "text", content: "dom mode" }
					},
				)
			})

			const context: PageContext = {
				url: new URL("http://localhost/dom"),
				params: {},
				mode: "dom",
			}

			await renderRoute(route)(context)

			assertEquals(capturedMode, "dom")
		},
	)
})

Deno.test(
	"renderRoute - property: result comes from page function",
	async function resultFromPageFunction() {
		const pathArb = fc
			.array(fc.stringMatching(/^[a-z0-9-]+$/), { minLength: 0, maxLength: 3 })
			.map(function toPath(segments: ReadonlyArray<string>): string {
				return "/" + segments.join("/")
			})

		await fc.assert(
			fc.asyncProperty(
				pathArb,
				fc.string(),
				async function checkResultFromPage(
					path: string,
					content: string,
				): Promise<boolean> {
					const route = mockRoute(path, content)
					const context = testContext(path)
					const result = await renderRoute(route)(context)

					return result._tag === "text" &&
						(result as { _tag: "text"; content: string }).content === content
				},
			),
		)
	},
)
