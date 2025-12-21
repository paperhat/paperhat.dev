//++ Type definitions for the routing system

import type { VirtualNode } from "@sitebender/architect/types/index.ts"

//++ The context passed to every page function
export type PageCtx = {
	readonly url: URL
	readonly params: Readonly<Record<string, string>>
	readonly mode: "dom" | "string"
}

//++ A page function takes context and returns a VirtualNode (Architect IR)
export type PageFn = (ctx: PageCtx) => VirtualNode

//++ A load function lazily imports a page module
export type LoadFn = () => Promise<PageFn>

//++ A route record associates a path with a lazy page loader
export type RouteRecord = {
	readonly path: string
	readonly load: LoadFn
}
