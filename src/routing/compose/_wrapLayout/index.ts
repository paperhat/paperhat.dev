import type { LayoutFunction, PageFunction } from "../../types/index.ts"

/*++
 + [EXCEPTION] Reducer callback accepts (accumulator, item) - NOT CURRIED as per Toolsmith reduceRight
 + Wraps accumulator page with layout function
 */
export default function _wrapLayout(
	acc: PageFunction,
	layout: LayoutFunction,
): PageFunction {
	return layout(acc)
}
