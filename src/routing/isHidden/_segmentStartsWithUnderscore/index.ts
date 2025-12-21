import _startsWithUnderscore from "../_startsWithUnderscore/index.ts"

//++ [EXCEPTION] Callback adapter for Toolsmith `some` predicate signature
export default function _segmentStartsWithUnderscore(
	segment: string,
	_index: number,
	_array: ReadonlyArray<string>,
): boolean {
	return _startsWithUnderscore(segment)
}
