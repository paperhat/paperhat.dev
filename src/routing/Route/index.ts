import type { LoadFn, RouteRecord } from "../types/index.ts"

//++ Creates a RouteRecord from a path and a lazy page loader
export default function Route(path: string) {
	return function RouteWithPath(load: LoadFn): RouteRecord {
		return {
			path,
			load,
		}
	}
}
