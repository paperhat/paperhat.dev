import { assertEquals } from "@std/assert"
import * as fc from "fast-check"

import Route from "./index.ts"
import type { PageFn } from "../types/index.ts"

Deno.test("Route", async function RouteTests(t) {
	await t.step(
		"creates a RouteRecord with path and load",
		function createsRouteRecord() {
			function mockLoad(): Promise<PageFn> {
				return Promise.resolve(function mockPage() {
					return { _tag: "text" as const, content: "test" }
				})
			}

			const route = Route("/about")(mockLoad)

			assertEquals(route.path, "/about")
			assertEquals(route.load, mockLoad)
		},
	)

	await t.step(
		"is curried - returns function after first call",
		function isCurried() {
			const withPath = Route("/")

			assertEquals(typeof withPath, "function")
		},
	)

	await t.step(
		"partial application preserves path",
		function partialApplicationWorks() {
			const withPath = Route("/users")

			function load1(): Promise<PageFn> {
				return Promise.resolve(function page1() {
					return { _tag: "text" as const, content: "1" }
				})
			}

			function load2(): Promise<PageFn> {
				return Promise.resolve(function page2() {
					return { _tag: "text" as const, content: "2" }
				})
			}

			const route1 = withPath(load1)
			const route2 = withPath(load2)

			assertEquals(route1.path, "/users")
			assertEquals(route2.path, "/users")
			assertEquals(route1.load, load1)
			assertEquals(route2.load, load2)
		},
	)

	await t.step(
		"load function is callable and returns Promise",
		async function loadIsCallable() {
			function mockLoad(): Promise<PageFn> {
				return Promise.resolve(function mockPage() {
					return { _tag: "text" as const, content: "loaded" }
				})
			}

			const route = Route("/test")(mockLoad)
			const pageFn = await route.load()
			const result = pageFn({
				url: new URL("http://localhost/test"),
				params: {},
				mode: "string",
			})

			assertEquals(result, { _tag: "text", content: "loaded" })
		},
	)
})

Deno.test("Route - property: path is preserved", function pathPreserved() {
	fc.assert(
		fc.property(fc.string(), function checkPathPreserved(path: string) {
			function mockLoad(): Promise<PageFn> {
				return Promise.resolve(function mockPage() {
					return { _tag: "text" as const, content: "" }
				})
			}

			const route = Route(path)(mockLoad)

			return route.path === path
		}),
	)
})

Deno.test(
	"Route - property: load function is preserved",
	function loadPreserved() {
		fc.assert(
			fc.property(fc.string(), function checkLoadPreserved(path: string) {
				function mockLoad(): Promise<PageFn> {
					return Promise.resolve(function mockPage() {
						return { _tag: "text" as const, content: "" }
					})
				}

				const route = Route(path)(mockLoad)

				return route.load === mockLoad
			}),
		)
	},
)
