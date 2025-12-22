import { COLLECT_INDEX_FILES_CODE } from "../constants/index.ts"

//++ Help code type for collectIndexFiles function
export type CollectIndexFilesHelpCode =
	typeof COLLECT_INDEX_FILES_CODE[keyof typeof COLLECT_INDEX_FILES_CODE]
