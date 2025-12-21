import type { VirtualNode } from "@sitebender/architect/types/index.ts"
import type { PageContext, RouteRecord } from "../types/index.ts"

//++ Renders a route by loading its page and applying context
export default function renderRoute(route: RouteRecord) {
	return async function renderRouteWithRoute(
		context: PageContext,
	): Promise<VirtualNode> {
		const page = await route.load()

		return page(context)
	}
}
