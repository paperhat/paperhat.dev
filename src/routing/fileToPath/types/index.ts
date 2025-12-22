import { FILE_TO_PATH_CODE } from "../constants/index.ts"

//++ Help code type for fileToPath function
export type FileToPathHelpCode =
	typeof FILE_TO_PATH_CODE[keyof typeof FILE_TO_PATH_CODE]
