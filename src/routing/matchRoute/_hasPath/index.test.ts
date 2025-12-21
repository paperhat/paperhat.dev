import { assertEquals } from "@std/assert"
import * as fc from "fast-check"

import _hasPath from "./index.ts"
import Route from "../../Route/index.ts"
import type { PageFunction, RouteRecord } from "../../types/index.ts"

//++ Helper to create a mock route
function mockRoute(path: string): RouteRecord {
	return Route(path)(function mockLoad(): Promise<PageFunction> {
		return Promise.resolve(function mockPage() {
			return { _tag: "text" as const, content: path }
		})
	})
}

Deno.test("_hasPath", async function hasPathTests(t) {
	await t.step(
		"returns true when route path matches target path",
		function returnsTrueWhenMatches() {
			const route = mockRoute("/about")
			const hasAboutPath = _hasPath("/about")

			assertEquals(hasAboutPath(route), true)
		},
	)

	await t.step(
		"returns false when route path does not match target path",
		function returnsFalseWhenNoMatch() {
			const route = mockRoute("/about")
			const hasContactPath = _hasPath("/contact")

			assertEquals(hasContactPath(route), false)
		},
	)

	await t.step(
		"is curried - returns function after first call",
		function isCurried() {
			const hasHomePath = _hasPath("/")

			assertEquals(typeof hasHomePath, "function")
		},
	)

	await t.step(
		"partial application allows reuse with same path",
		function partialApplicationWorks() {
			const hasAboutPath = _hasPath("/about")
			const aboutRoute = mockRoute("/about")
			const homeRoute = mockRoute("/")
			const contactRoute = mockRoute("/contact")

			assertEquals(hasAboutPath(aboutRoute), true)
			assertEquals(hasAboutPath(homeRoute), false)
			assertEquals(hasAboutPath(contactRoute), false)
		},
	)

	await t.step(
		"matches exact paths only",
		function matchesExactPaths() {
			const hasAboutPath = _hasPath("/about")

			assertEquals(hasAboutPath(mockRoute("/about")), true)
			assertEquals(hasAboutPath(mockRoute("/about/")), false)
			assertEquals(hasAboutPath(mockRoute("/about/team")), false)
			assertEquals(hasAboutPath(mockRoute("about")), false)
		},
	)
})

Deno.test(
	"_hasPath - property: matching path returns true",
	function matchingPathReturnsTrue() {
		fc.assert(
			fc.property(fc.string(), function checkMatchingPath(path: string) {
				const route = mockRoute(path)
				const hasTargetPath = _hasPath(path)

				return hasTargetPath(route) === true
			}),
		)
	},
)

Deno.test(
	"_hasPath - property: different path returns false",
	function differentPathReturnsFalse() {
		fc.assert(
			fc.property(
				fc.string(),
				fc.string(),
				function checkDifferentPath(path1: string, path2: string) {
					fc.pre(path1 !== path2)

					const route = mockRoute(path1)
					const hasPath2 = _hasPath(path2)

					return hasPath2(route) === false
				},
			),
		)
	},
)
