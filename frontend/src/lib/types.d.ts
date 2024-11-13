import { OutputType } from "@/components/single-code/types";

export type GetSingleGenerationResponse = {
  type: OutputType;
  content: string;
};

export type GenerateGithubWebsiteResponse = {
  url: string;
  success: string;
};
