import type { WalkEntry } from "@std/fs"
import type { BaseHelp } from "@sitebender/toolsmith/help/types/index.ts"
import type { AsyncIoResult } from "@sitebender/toolsmith/monads/io/types/index.ts"
import type { Result } from "@sitebender/toolsmith/monads/result/types/index.ts"

import { SEVERITY } from "@sitebender/toolsmith/help/constants/index.ts"
import asyncIoResult from "@sitebender/toolsmith/monads/io/asyncIoResult/index.ts"
import createHelp from "@sitebender/toolsmith/help/createHelp/index.ts"
import help from "@sitebender/toolsmith/monads/result/help/index.ts"
import isString from "@sitebender/toolsmith/guards/type/isString/index.ts"
import not from "@sitebender/toolsmith/logic/not/index.ts"
import ok from "@sitebender/toolsmith/monads/result/ok/index.ts"
import { walk } from "@std/fs"

import isHidden from "../isHidden/index.ts"
import { COLLECT_INDEX_FILES_CODE } from "./constants/index.ts"
import type { CollectIndexFilesHelpCode } from "./types/index.ts"

//++ [EXCEPTION] Uses Array.from, filter, and map methods inside async IO boundary
//++ Collects all non-hidden index.ts files from a directory
export default function collectIndexFiles(
	root: unknown,
): AsyncIoResult<BaseHelp<CollectIndexFilesHelpCode>, ReadonlyArray<string>> {
	if (isString(root)) {
		return asyncIoResult(
			async function executeCollectIndexFiles(): Promise<
				Result<BaseHelp<CollectIndexFilesHelpCode>, ReadonlyArray<string>>
			> {
				try {
					const walkIterable = walk(root, {
						exts: [".ts"],
						match: [/index\.ts$/],
					})

					const entries: Array<WalkEntry> = []

					for await (const entry of walkIterable) {
						entries.push(entry)
					}

					const paths = entries
						.filter(function filterVisible(entry: WalkEntry): boolean {
							return not(isHidden(entry.path))
						})
						.map(function extractPath(entry: WalkEntry): string {
							return entry.path
						})

					return ok(paths)
				} catch (_err) {
					return help(
						createHelp(COLLECT_INDEX_FILES_CODE.walkFailed)(
							"Failed to walk directory",
						)(SEVERITY.critical),
					)
				}
			},
		)
	}

	return asyncIoResult(function returnRootNotStringHelp(): Promise<
		Result<BaseHelp<CollectIndexFilesHelpCode>, ReadonlyArray<string>>
	> {
		return Promise.resolve(
			help(
				createHelp(COLLECT_INDEX_FILES_CODE.rootNotString)(
					"Root path must be a string",
				)(SEVERITY.critical),
			),
		)
	})
}
