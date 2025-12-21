import type { RouteRecord } from "../../types/index.ts"

//++ Checks if a route's path matches the target path
export default function _hasPath(path: string) {
	return function _hasPathWithPath(route: RouteRecord): boolean {
		return route.path === path
	}
}
