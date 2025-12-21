import type { LayoutFunction, PageFunction } from "../types/index.ts"

import reduceRight from "@sitebender/toolsmith/array/reduceRight/index.ts"
import getOrElse from "@sitebender/toolsmith/monads/maybe/getOrElse/index.ts"
import just from "@sitebender/toolsmith/monads/maybe/just/index.ts"
import _wrapLayout from "./_wrapLayout/index.ts"

//++ Composes an array of layout functions with a page, right-to-left
export default function compose(layouts: ReadonlyArray<LayoutFunction>) {
	return function composeWithLayouts(page: PageFunction): PageFunction {
		return getOrElse<PageFunction>(page)(
			reduceRight<LayoutFunction, PageFunction>(_wrapLayout)(page)(
				just(layouts),
			),
		)
	}
}
