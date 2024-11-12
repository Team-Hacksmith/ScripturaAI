import { OutputType } from "@/components/single-code/types";

export const BASE_URL = process.env.BASE_URL || "http://127.0.0.1:5000";

export const supported_languages = [
  "python",
  "cpp",
  "c",
  "java",
  "javascript",
  "typescript",
  "rust",
  "go",
  "kotlin",
  "swift",
];

export const supported_types: OutputType[] = [
  "code",
  "algo",
  "guide",
  "diagram",
];
