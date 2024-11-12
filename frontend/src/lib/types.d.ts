import { OutputType } from "@/components/single-code/types";

export type GetSingleGenerationResponse = {
  type: OutputType;
  content: string;
};
