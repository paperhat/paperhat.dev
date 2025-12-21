import getOrElse from "@sitebender/toolsmith/monads/maybe/getOrElse/index.ts"
import just from "@sitebender/toolsmith/monads/maybe/just/index.ts"
import startsWith from "@sitebender/toolsmith/string/startsWith/index.ts"

//++ Predicate: checks if string starts with underscore
export default function _startsWithUnderscore(segment: string): boolean {
	return getOrElse(false)(startsWith(0)("_")(just(segment)))
}
