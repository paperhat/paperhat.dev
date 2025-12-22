import type { BaseHelp } from "@sitebender/toolsmith/help/types/index.ts"
import type { AsyncIoResult } from "@sitebender/toolsmith/monads/io/types/index.ts"
import type { Result } from "@sitebender/toolsmith/monads/result/types/index.ts"

import { SEVERITY } from "@sitebender/toolsmith/help/constants/index.ts"
import asyncIoResult from "@sitebender/toolsmith/monads/io/asyncIoResult/index.ts"
import createHelp from "@sitebender/toolsmith/help/createHelp/index.ts"
import help from "@sitebender/toolsmith/monads/result/help/index.ts"
import isString from "@sitebender/toolsmith/guards/type/isString/index.ts"
import ok from "@sitebender/toolsmith/monads/result/ok/index.ts"
import { walk } from "@std/fs"

import isHidden from "../isHidden/index.ts"
import { COLLECT_INDEX_FILES_CODE } from "./constants/index.ts"
import type { CollectIndexFilesHelpCode } from "./types/index.ts"

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
					const files: Array<string> = []

					for await (
						const entry of walk(root, {
							exts: [".ts"],
							match: [/index\.ts$/],
						})
					) {
						if (isHidden(entry.path)) {
							continue
						}

						files.push(entry.path)
					}

					return ok(files)
				} catch (error) {
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
