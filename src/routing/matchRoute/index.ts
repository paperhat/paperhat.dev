import type { Maybe } from "@sitebender/toolsmith/monads/maybe/types/index.ts"
import type { RouteRecord } from "../types/index.ts"

import find from "@sitebender/toolsmith/array/find/index.ts"
import just from "@sitebender/toolsmith/monads/maybe/just/index.ts"

//++ Finds the first route matching the given path, returns Maybe<RouteRecord>
export default function matchRoute(routes: ReadonlyArray<RouteRecord>) {
	return function matchRouteIn(path: string): Maybe<RouteRecord> {
		function hasPath(route: RouteRecord): boolean {
			return route.path === path
		}

		return find<RouteRecord, never>(hasPath)(just(routes))
	}
}
