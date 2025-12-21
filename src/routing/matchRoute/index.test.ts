import { assertEquals } from "@std/assert"
import * as fc from "fast-check"

import isJust from "@sitebender/toolsmith/monads/maybe/guards/isJust/index.ts"
import isNothing from "@sitebender/toolsmith/monads/maybe/guards/isNothing/index.ts"

import matchRoute from "./index.ts"
import Route from "../Route/index.ts"
import type { PageFunction, RouteRecord } from "../types/index.ts"

//++ Helper to create a mock route
function mockRoute(path: string): RouteRecord {
	return Route(path)(function mockLoad(): Promise<PageFunction> {
		return Promise.resolve(function mockPage() {
			return { _tag: "text" as const, content: path }
		})
	})
}

Deno.test("matchRoute", async function matchRouteTests(t) {
	await t.step(
		"returns Just when route is found",
		function returnsJustWhenFound() {
			const routes = [
				mockRoute("/"),
				mockRoute("/about"),
				mockRoute("/contact"),
			]
			const result = matchRoute(routes)("/about")

			assertEquals(isJust(result), true)
			if (isJust(result)) {
				assertEquals(result.value.path, "/about")
			}
		},
	)

	await t.step(
		"returns Nothing when route is not found",
		function returnsNothingWhenNotFound() {
			const routes = [mockRoute("/"), mockRoute("/about")]
			const result = matchRoute(routes)("/nonexistent")

			assertEquals(isNothing(result), true)
		},
	)

	await t.step(
		"returns Nothing when routes array is empty",
		function returnsNothingWhenEmpty() {
			const routes: ReadonlyArray<RouteRecord> = []
			const result = matchRoute(routes)("/any")

			assertEquals(isNothing(result), true)
		},
	)

	await t.step(
		"finds first matching route",
		function findsFirstMatch() {
			const routes = [mockRoute("/"), mockRoute("/about"), mockRoute("/about")]
			const result = matchRoute(routes)("/about")

			assertEquals(isJust(result), true)
			if (isJust(result)) {
				assertEquals(result.value.path, "/about")
				assertEquals(result.value, routes[1])
			}
		},
	)

	await t.step(
		"is curried - returns function after first call",
		function isCurried() {
			const routes = [mockRoute("/")]
			const findRoute = matchRoute(routes)

			assertEquals(typeof findRoute, "function")
		},
	)

	await t.step(
		"partial application allows reuse with same routes",
		function partialApplicationWorks() {
			const routes = [
				mockRoute("/"),
				mockRoute("/about"),
				mockRoute("/contact"),
			]
			const findRoute = matchRoute(routes)

			const home = findRoute("/")
			const about = findRoute("/about")
			const missing = findRoute("/missing")

			assertEquals(isJust(home), true)
			assertEquals(isJust(about), true)
			assertEquals(isNothing(missing), true)
		},
	)

	await t.step(
		"matches exact paths only",
		function matchesExactPaths() {
			const routes = [mockRoute("/about")]

			assertEquals(isNothing(matchRoute(routes)("/about/")), true)
			assertEquals(isNothing(matchRoute(routes)("/about/team")), true)
			assertEquals(isNothing(matchRoute(routes)("about")), true)
			assertEquals(isJust(matchRoute(routes)("/about")), true)
		},
	)
})

Deno.test(
	"matchRoute - property: found route has matching path",
	function foundRouteHasMatchingPath() {
		fc.assert(
			fc.property(
				fc.array(fc.string(), { minLength: 1 }),
				function checkFoundRouteMatches(paths: ReadonlyArray<string>) {
					const routes = paths.map(mockRoute)
					const targetPath = paths[0]

					if (targetPath === undefined) {
						return true
					}

					const result = matchRoute(routes)(targetPath)

					if (isJust(result)) {
						return result.value.path === targetPath
					}
					return false
				},
			),
		)
	},
)

Deno.test(
	"matchRoute - property: Nothing means no route has path",
	function nothingMeansNoMatch() {
		fc.assert(
			fc.property(
				fc.array(fc.string()),
				fc.string(),
				function checkNothingMeansNoMatch(
					paths: ReadonlyArray<string>,
					searchPath: string,
				) {
					const routes = paths.map(mockRoute)
					const result = matchRoute(routes)(searchPath)

					if (isNothing(result)) {
						return paths.every(function pathNotEqual(p: string) {
							return p !== searchPath
						})
					}
					return true
				},
			),
		)
	},
)
