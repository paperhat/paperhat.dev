//++ Type definitions for the routing system
import type { VirtualNode } from "@sitebender/architect/types/index.ts"

//++ The context passed to every page function
export type PageContext = {
	readonly url: URL
	readonly params: Readonly<Record<string, string>>
	readonly mode: "dom" | "string"
}

//++ A page function takes context and returns a VirtualNode (Architect IR)
export type PageFunction = (context: PageContext) => VirtualNode

//++ A layout function wraps a child page and returns a new page function
export type LayoutFunction = (child: PageFunction) => PageFunction

//++ A load function lazily imports a page module
export type LoadFunction = () => Promise<PageFunction>

//++ A route record associates a path with a lazy page loader
export type RouteRecord = {
	readonly path: string
	readonly load: LoadFunction
}
