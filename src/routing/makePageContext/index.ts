import type { PageContext } from "../types/index.ts"

//++ Curried factory for creating PageContext values
export default function makePageContext(url: URL) {
	return function makePageContextWithUrl(
		params: Readonly<Record<string, string>>,
	) {
		return function makePageContextWithUrlAndParams(
			mode: "dom" | "string",
		): PageContext {
			return { url, params, mode }
		}
	}
}
