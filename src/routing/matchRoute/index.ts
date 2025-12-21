import type { Maybe } from "@sitebender/toolsmith/monads/maybe/types/index.ts"
import type { RouteRecord } from "../types/index.ts"

import find from "@sitebender/toolsmith/array/find/index.ts"
import just from "@sitebender/toolsmith/monads/maybe/just/index.ts"
import _hasPath from "./_hasPath/index.ts"

//++ Finds the first route matching the given path, returns Maybe<RouteRecord>
export default function matchRoute(routes: ReadonlyArray<RouteRecord>) {
	return function matchRouteWithRoutes(path: string): Maybe<RouteRecord> {
		return find<RouteRecord, never>(_hasPath(path))(just(routes))
	}
}
