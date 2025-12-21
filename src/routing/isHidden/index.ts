import getOrElse from "@sitebender/toolsmith/monads/maybe/getOrElse/index.ts"
import just from "@sitebender/toolsmith/monads/maybe/just/index.ts"
import isString from "@sitebender/toolsmith/guards/type/isString/index.ts"
import some from "@sitebender/toolsmith/array/some/index.ts"
import split from "@sitebender/toolsmith/string/split/index.ts"

import _segmentStartsWithUnderscore from "./_segmentStartsWithUnderscore/index.ts"

//++ Predicate: checks if any path segment starts with underscore
export default function isHidden(value: unknown): boolean {
	if (isString(value)) {
		return getOrElse(false)(
			some(_segmentStartsWithUnderscore)(
				split(Number.MAX_SAFE_INTEGER)("/")(just(value)),
			),
		)
	}

	return false
}
