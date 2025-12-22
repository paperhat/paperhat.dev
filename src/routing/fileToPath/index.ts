import type { BaseHelp } from "@sitebender/toolsmith/help/types/index.ts"
import type { Result } from "@sitebender/toolsmith/monads/result/types/index.ts"

import { SEVERITY } from "@sitebender/toolsmith/help/constants/index.ts"
import createHelp from "@sitebender/toolsmith/help/createHelp/index.ts"
import help from "@sitebender/toolsmith/monads/result/help/index.ts"
import isString from "@sitebender/toolsmith/guards/type/isString/index.ts"
import ok from "@sitebender/toolsmith/monads/result/ok/index.ts"
import { dirname, relative } from "@std/path"

import { FILE_TO_PATH_CODE } from "./constants/index.ts"
import type { FileToPathHelpCode } from "./types/index.ts"

//++ Converts a file path to a route path relative to root
export default function fileToPath(root: unknown) {
	return function fileToPathWithRoot(
		file: unknown,
	): Result<BaseHelp<FileToPathHelpCode>, string> {
		if (isString(root)) {
			if (isString(file)) {
				const relativePath = relative(root, file)
				const dir = dirname(relativePath)
				const routePath = dir === "." ? "/" : "/" + dir

				return ok(routePath)
			}

			return help(
				createHelp(FILE_TO_PATH_CODE.fileNotString)(
					"File path must be a string",
				)(SEVERITY.critical),
			)
		}

		return help(
			createHelp(FILE_TO_PATH_CODE.rootNotString)(
				"Root path must be a string",
			)(SEVERITY.critical),
		)
	}
}
